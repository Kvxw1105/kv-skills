---
name: kv-goal-loop
description: >
  Goal Mode / Loop Engineering 自主循环执行引擎。将高层目标转为自主循环：
  计划→执行→验证→评估→迭代，直到目标达成或预算耗尽。
  核心设计：执行者与评判者分离、停滞检测、上下文压缩、文件化状态。
  当用户设定高层目标、要求"goal mode"、"自主循环"、"做到完成为止"、
  "loop engineering"、"自动迭代"、"无人值守执行"、"持续优化直到"、
  "跑个循环"、"自动执行直到完成"时触发。也适用于：复杂多步骤任务需要
  自主分解并反复验证迭代的场景。不适用于：单步简单任务、一次性问答。
version: 1.0.0
metadata:
  ip-prefix: kv
  author: "心吾"
  visibility: public
  role: product
  publish_target: kv-skills
  memory_policy: public
---

# Goal Loop — 自主循环执行引擎

受 Codex CLI Goal Mode、OpenHands、SWE-agent 启发的 Loop Engineering 实现。
核心原则：**循环本身不是魔法，循环内的反馈才是。**

## 适用场景

- 用户设定高层目标，需要自主分解并多轮迭代
- "做到完成为止" / "goal mode" / "loop" / "自主循环"
- 复杂任务需要自主 计划→执行→验证→评估→再迭代
- 需要"无人值守"长时间运行
- 明确不需要：单步任务、一次性代码修改、纯问答

## 核心架构

```
┌──────────────────────────────────────────────────────┐
│                    GOAL LOOP                          │
│                                                       │
│  ┌────────┐    ┌─────────┐    ┌──────────┐           │
│  │  PLAN  │───▶│ EXECUTE │───▶│  VERIFY  │           │
│  └────▲───┘    └─────────┘    └─────┬────┘           │
│       │                             │                 │
│       │    ┌───────────┐            │                 │
│       └────┤ EVALUATE  │◀───────────┘                 │
│            └─────┬─────┘                              │
│                  │                                    │
│         ┌────────┴────────┐                           │
│         ▼                 ▼                           │
│      [PASS]             [FAIL]                        │
│        │                  │                           │
│     ✅ DONE         🔄 Back to PLAN                   │
│                    (with evaluator feedback)          │
│                                                       │
│  ── 退出守卫 ──                                       │
│  预算耗尽 │ 连续停滞≥3 │ 目标达成 │ 用户中断          │
└──────────────────────────────────────────────────────┘
```

## MCP Runtime 集成（持久循环关键）

如果当前环境有 `goal-loop-orchestrator` MCP server 可用，**必须使用 MCP 工具管理循环**，而不是自行管理。这是循环不断掉的核心机制。

### MCP 工具调用时机

| Phase | MCP 工具调用 | 作用 |
|-------|-------------|------|
| Phase 0 结束 | `start_loop(goal, success_criteria, max_rounds)` | 创建循环，获得 loop_id |
| Phase 4 评估前 | `get_evaluator_context(loop_id, outputs, verification)` | 生成评估 prompt |
| Phase 4 评估后 | `end_round(loop_id, verified, evaluated, summary, feedback)` | **核心驱动点** — 返回下一步指令 |
| 每轮开始 | `get_loop_state(loop_id)` | 恢复上下文状态 |
| 需要时 | `check_stagnation(loop_id)` | 停滞诊断 |

### 关键规则

1. **`end_round` 的返回决策是 BINDING 的** — 如果它说 CONTINUE，你**必须**开始下一轮，不能停下来等用户
2. **如果 MCP 不可用**，回退到文件化状态（GOAL.md + loop-state.md），但循环可能中断
3. **每轮结束必须调用 `end_round`** — 这是外部循环驱动器的唯一接入点

### 无 MCP 时的降级

如果没有 goal-loop-orchestrator MCP，使用 Phase 0-6 的文件协议手动管理循环。效果会打折扣——循环可能在某轮后中断。

## 执行协议

### Phase 0: 初始化 — 写 GOAL.md

用户给出目标后，在工作目录创建 `GOAL.md`（模板见下方）。**所有成功标准必须可机器验证**。

**MCP 集成**：GOAL.md 创建后，立即调用 `start_loop(goal, success_criteria, max_rounds)` 注册循环。记录返回的 `loop_id`。

如果用户只给了模糊目标，必须先追问使其可验证：
- ❌ "改善代码质量" → 无验证手段
- ✅ "所有 79 个 pytest 测试通过，coverage ≥ 80%，0 个 ruff 错误"
- ❌ "做一个好看的页面" → 无验证手段
- ✅ "Lighthouse Performance ≥ 90，所有页面在 Chrome/Safari 无布局偏移，WCAG AA 对比度达标"

### Phase 1: 创建执行计划（Plan）

根据目标类型选择计划方式：

| 目标类型 | 计划方式 |
|---------|---------|
| 软件开发（新功能/重构） | 使用结构化的实现计划方法论 |
| Bug 修复 | 直接定位→修复→验证，无需完整计划 |
| 研究/分析 | 分解为独立调研子任务 |
| 通用 | 用任务追踪器或文件分解为 ≤10 个原子任务 |

**原则：每轮迭代只做增量改进，不贪多。首轮做最高优先级的 3-5 个任务。**

### Phase 2: 执行（Execute）

按计划执行任务。选择执行策略：

- **单线程顺序执行**：任务间有依赖时
- **并行子 Agent**：独立子任务时，spawn 多个子 Agent 并行执行（如果 Agent 支持）
- **混合模式**：先并行独立子任务，再顺序执行依赖任务

执行过程中实时更新任务追踪器。每完成一个原子任务，立即进入验证。

### Phase 3: 验证（Verify）

**每个任务完成后立即验证**，不等全部完成。验证手段按优先级：

1. **测试套件**：`pytest` / `npm test` / 项目测试命令
2. **Lint/Type Check**：`ruff` / `eslint` / `tsc` / 项目 lint 命令
3. **Build Check**：项目构建命令
4. **断言检查**：GOAL.md 中定义的成功标准逐条检查
5. **文件 diff**：对比预期产出与实际产出

验证结果记录到 `execution-log.md`。

### Phase 4: 独立评估（Evaluate）⚠️ 关键步骤

**跳过此步骤是最大反模式。** 自我评估几乎总是过于乐观。

#### MCP 集成（优先使用）

1. 调用 `get_evaluator_context(loop_id, current_outputs, verification_results)` 获取评估 prompt
2. Spawn 评估子 Agent，传入该 prompt
3. 将子 Agent 返回作为 `evaluator_feedback`
4. 调用 `end_round(loop_id, verified, evaluated, summary, evaluator_feedback)` — **这是循环驱动点**
5. `end_round` 返回的 `next_action.decision` 是 **BINDING** 的：
   - `CONTINUE` → 立即开始下一轮，不停
   - `COMPLETE` → 进入 Phase 6
   - `PAUSE_FOR_USER` → 展示诊断，等用户
   - `BUDGET_EXHAUSTED` / `STAGNATION_EXIT` → 输出最佳尝试

#### 降级模式（无 MCP 时）

Spawn 评估子 Agent，传入以下 context：

```
你是一个独立评估员。你只看到结果，不知道过程。

## 目标
{从 GOAL.md 的 # Objective 和 ## Success Criteria 提取}

## 当前产出
{列出完成的任务、修改的文件、测试结果等客观事实}

## 验证结果
{测试输出、lint 结果、build 状态等机器验证结果}

## 你需要回答
1. 每个成功标准是否已满足？逐条判断（Yes/No/Partial + 原因）
2. 是否存在未检查到的边界情况或遗漏？
3. 整体判断：GOAL_ACHIEVED / PARTIAL / NOT_ACHIEVED
4. 如果未达标：最需要改进的 1-2 个具体方向（不要泛泛而谈）
```

2. **评估结果处理**：

| 评估结果 | 动作 |
|---------|------|
| GOAL_ACHIEVED | 进入 Phase 6 收尾 |
| PARTIAL | 记录反馈，进入下一轮迭代 |
| NOT_ACHIEVED | 记录反馈 + 停滞检测 |

### Phase 5: 停滞检测与迭代决策

#### 停滞检测协议

维护 `loop-state.md` 中的 `consecutive_failures` 计数：

```
连续失败 1 次 → 根据评估反馈调整方案，继续
连续失败 2 次 → 强制切换方法（换算法/架构/工具链）
连续失败 3 次 → 暂停循环，请求用户介入，提供诊断摘要
连续失败 5 次 → 强制退出，输出最佳尝试 + 完整失败分析
```

#### 停滞诊断模板

当连续失败 ≥ 2 时，执行停滞分析：

```markdown
## 停滞诊断 (Round {N})

### 失败模式
- Round N-2: {失败原因}
- Round N-1: {失败原因}
- Round N: {失败原因}

### 根因分析
{分析是否是同一根因导致的反复失败，还是每次都是新问题}

### 建议
- 如果是同一根因：切换方法（具体建议 A / B / C）
- 如果是新问题：继续当前方法，修复新发现
- 如果超出能力：请求用户介入，提供具体信息
```

#### 迭代决策树

```
验证通过 + 评估通过 → 完成
验证通过 + 评估未通过 → 根据反馈调整，下一轮
验证未通过 + 新类型错误 → 修复错误，下一轮
验证未通过 + 重复错误 → 切换方法
切换方法后仍失败 → 请求用户介入
```

### Phase 6: 收尾

目标达成后：

1. **最终验证**：完整跑一遍所有成功标准的验证
2. **清理**：删除临时文件、确保工作区干净
3. **写总结**：在 `execution-log.md` 追加最终摘要
4. **更新 GOAL.md**：状态改为 completed
5. **记忆沉淀**：如果有值得跨会话保留的经验，写入记忆系统

## 文件协议

### GOAL.md 模板

在工作目录创建。这是循环的"宪法"，所有决策以此为据。

```markdown
# Goal

{一句话描述目标}

## Success Criteria

- [ ] {可机器验证的标准 1}
- [ ] {可机器验证的标准 2}
- [ ] {可机器验证的标准 3}

## Exit Conditions

- max_rounds: 5
- max_consecutive_failures: 3
- budget_type: rounds

## Context

- project: {项目名}
- working_dir: {工作目录}
- key_files: [{关键文件列表}]

## Current State

- status: in_progress
- current_round: 0
- consecutive_failures: 0
- last_evaluator_feedback: ""

## Iteration Log

### Round 0 — {timestamp}
- Plan: {本轮计划}
- Done: {完成项}
- Verified: {验证结果: pass/fail}
- Evaluated: {评估结果: GOAL_ACHIEVED/PARTIAL/NOT_ACHIEVED}
- Feedback: {评估员反馈摘要}
```

### execution-log.md

每轮迭代的详细记录。这是唯一的完整历史，用于跨迭代恢复上下文。

```markdown
# Execution Log

## Round {N} — {timestamp}

### Plan
{本轮执行的计划和原因}

### Actions Taken
{具体执行了什么}

### Verification
{验证命令和结果}

### Evaluation
{评估员完整反馈}

### Decision
{下一轮决策和原因}
```

### loop-state.md（轻量状态文件）

只包含恢复所需的最小信息。每轮结束更新。

```markdown
# Loop State
- round: {N}
- status: in_progress | completed | stalled | failed
- started: {ISO timestamp}
- last_updated: {ISO timestamp}
- consecutive_failures: {N}
- total_tasks_completed: {N}
- total_tasks_remaining: {N}
- approach_changes: {N}
```

## 上下文压缩协议

**这是避免 token 膨胀的关键。**

每轮迭代结束时：
1. 将本轮摘要写入 `execution-log.md`
2. 更新 `loop-state.md`
3. 下一轮开始时，只读取：GOAL.md（目标+标准）+ loop-state.md（当前状态）+ execution-log.md 最近一轮

**不要做的事：**
- 不要把完整执行日志带进下一轮
- 不要在对话中积累所有历史
- 不要把子 Agent 的完整输出带入主循环（只取结论）

## 可选增强

如果当前 Agent 环境中有以下能力，可在对应阶段调用以增强效果：

| 阶段 | 可选增强 | 作用 |
|------|----------|------|
| Plan | 实现计划类 Skill | 复杂项目的结构化计划生成 |
| Execute | 分批执行类 Skill | 带检查点的分批执行 |
| Execute (并行) | 多 Agent 协作类 Skill | 并行子任务编排 |
| Verify | 产品体验审查类 Skill | 从用户角度审查产出质量 |
| Evaluate | 盲点检测类 Skill | 识别评估中的确认偏误 |
| 代码质量 | 判断力增强类 Skill | 提升决策质量 |

**调用是可选的**——只在能明确增值时使用，不要为了用而用。

## 反模式清单

| 反模式 | 为什么错 | 正确做法 |
|--------|---------|---------|
| 跳过独立评估 | 自我评估总是过于乐观 | 永远 spawn 评估子 Agent |
| 用"步数"当退出条件 | 不知道多少步够 | 用"轮次"或"预算" |
| 不压缩上下文 | token 会爆炸 | 文件化状态，每轮只加载摘要 |
| 同方法重试 3+ 次 | 定义上的愚蠢 | 强制切换方法或求助 |
| 模糊成功标准 | 无法自动判断完成 | 所有标准必须可机器验证 |
| 一轮做太多 | 难定位问题 | 每轮 3-5 个原子任务 |
| 评估者看到过程 | 确认偏误 | 只传结果，不传推理历史 |

## 使用示例

### 简单示例

用户："帮我给 ai-skills-workbench 加上搜索功能，所有测试通过"

→ 创建 GOAL.md（成功标准：搜索 API 端点返回结果、前端搜索框可用、79 个 pytest 全过）
→ Round 1: 实现搜索 API + 单元测试 → 验证测试 → 评估
→ Round 2: 实现前端搜索 UI → 验证全部测试 → 评估
→ Round 3（如需要）: 修复评估反馈的问题 → 验证 → 评估通过 → 完成

### 复杂示例

用户："重构这个 React 组件，保持所有现有功能，性能提升 50%"

→ GOAL.md（成功标准：所有现有 E2E 测试通过、Lighthouse 性能分 ≥ 90、无功能回归）
→ Round 1: 性能 profiling + 瓶颈分析 → 定位热点 → 评估方向
→ Round 2: 实现优化（memo/虚拟列表/懒加载）→ 测试 + profiling → 评估
→ Round 3: 微调 + 边界 case 修复 → 完整测试 → 评估通过 → 完成
