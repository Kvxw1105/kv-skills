---
name: kv-engineering-reasoning-harness
description: Strengthen software-engineering planning, coding, debugging, review, recovery, retrospective, and handoff for coding agents, especially weaker or context-limited models. Use for Codex or other repository agents when starting a project, planning a feature, continuing an interrupted task, implementing code, diagnosing failures, reviewing a change, completing a milestone, producing a handoff, designing AGENTS.md or persistent project instructions, or preventing shallow reasoning, unsafe edits, scope drift, and false completion claims. Trigger on requests such as 开发规划、项目接力、节点复盘、接管仓库、继续开发、低模型增智、深度思考后编码、handoff、recovery、plan before coding, verify the implementation, or create an engineering harness.
---

# 工程推理与接力增强器

把工程任务转换为可核验的闭环：**核验现状 → 明确目标 → 选择路径 → 最小实现 → 分层验证 → 反方审查 → 状态交接**。

本 Skill 的重点是提高低能力模型的可靠性。不要用空泛的“深入思考”代替流程、证据和检查点。

## 核心纪律

1. 先观察，后推断；先搜索现有模式，后新增抽象。
2. 保护用户工作。未提交修改、数据、密钥、配置和明确保护区默认不可恢复、删除、覆盖、暂存或提交。
3. 将状态标记为 `OBSERVED`、`INFERRED`、`PLANNED`、`COMPLETED` 或 `BLOCKED`。
4. 将完成层级分开陈述：代码修改、本地验证、commit、push、PR、CI、release 不得合并成“已完成”。
5. 优先交付最小但完整的可验证切片，避免一次铺开多个未闭环方向。
6. 结论必须对应证据。无法运行验证时，明确替代检查和剩余风险。
7. 不输出隐藏思维链。输出决策、依据、证据、风险和下一步。

## 工作流

### 1. 路由工作模式

先判断一个主模式，可串联一个或多个后续模式：

- `INIT`：新项目或新能力开局
- `RECOVERY`：上下文丢失、会话中断、旧交接不可信
- `PLAN`：制定实现路线、拆解节点或比较方案
- `IMPLEMENT`：修改代码并形成真实增量
- `DEBUG`：复现、定位和修复故障
- `REVIEW`：审查方案、代码、测试或交付质量
- `RETRO`：复盘节点、提炼规则和技术债
- `HANDOFF`：为下一个人或 Agent 留下可继续状态

读取 [operating-modes.md](references/operating-modes.md) 获取模式判定和检查表。

### 2. 核验当前现实

在中大型任务或现有仓库中，先检查：

- 工作目录、仓库根、分支、commit、worktree 和 `git status`
- 适用的 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、仓库指令、README、CONTRIBUTING 和局部规则
- 与任务直接相关的入口、调用链、数据流、配置、测试和构建脚本
- 相关 issue、PR、review、commit、TODO、日志和旧交接
- 用户明确保护的文件、接口、数据和行为

不要只阅读目录树。至少找到当前任务的关键调用链或行为路径。

### 3. 建立状态账本

在动手前形成简洁账本：

- **目标**：用户最终需要的可观察结果
- **现状**：已证实的能力、缺口和工作区风险
- **不变量**：必须保持兼容或不可触碰的内容
- **未知项**：会改变实现路径的关键未知
- **验收**：怎样证明任务成立
- **最小切片**：当前轮次最小完整交付

对可逆、低风险的小缺口使用明确假设继续推进。涉及数据丢失、公开接口、生产权限或不可逆架构时，停止破坏性动作并说明阻塞。

### 4. 制定依赖有序的计划

当任务跨多个文件、需要架构选择、预计超过一个短闭环或用户明确要求规划时，读取 [planning.md](references/planning.md)。

计划必须包含：

- 当前状态和目标状态
- 非目标与边界
- 方案比较与明确推荐
- 依赖顺序
- 每步交付物、完成标准和验证方式
- 风险、回滚或降级路径

不要把“优化、完善、增强”当作可执行目标。

### 5. 执行最小完整切片

进入实现或调试时，读取 [implementation-debugging.md](references/implementation-debugging.md)。

执行规则：

- 先搜索相似组件、接口、测试、错误处理和命名约定。
- 一轮只推进一个主要目标；控制文件和依赖改动半径。
- 修改后检查实际 diff，排除无关格式化、调试残留、密钥和本地路径。
- 调试时先稳定复现，再提出少量假设；一次验证一个关键变量。
- 连续两次尝试未缩小问题时，停止盲改，回到 `RECOVERY` 或 `PLAN` 重建假设。

### 6. 分层验证并校准完成状态

任何运行时代码、测试、构建配置或行为变化，在声称完成前读取 [verification-evidence.md](references/verification-evidence.md)。

按风险选择验证层级：静态检查、类型检查、lint、针对性测试、模块测试、集成测试、构建、实际运行、浏览器或端到端验证、扩大回归。

记录命令、结果、失败归因和未验证内容。只达到哪一层，就声称哪一层。

### 7. 进行反方审查

实现后用审查者视角检查一次：

- 是否误解目标或只实现表面路径
- 是否破坏兼容性、权限、状态或数据
- 是否遗漏错误路径、边界条件、并发和时序
- 测试是否证明需求成立，而非仅证明代码能运行
- 是否引入过度抽象或隐性维护成本
- 是否把推断写成事实

复杂任务最多执行三轮“实现 → 验证 → 审查 → 修正”。

### 8. 更新项目记忆并交接

节点结束、切换模型、会话中断或用户要求复盘时，读取 [retrospective-handoff.md](references/retrospective-handoff.md)。

交接必须精确记录：项目位置、分支和 commit；本轮目标；关键修改；验证证据；Git 七级状态；未完成事项；保护区；下一步前三项；接管启动指令。

## 低能力模型增强协议

当模型能力有限、上下文庞大或任务容易失控时，自动收紧流程：

1. 将大任务拆成可独立验证的小节点，每个节点只保留一个主要目标。
2. 把关键事实、不变量、未知项和决策写入文件或状态账本，避免依赖会话记忆。
3. 每次编辑前说明预期行为变化；编辑后用 diff 和测试核对。
4. 不凭印象跨越调用链。搜索定义、引用、入口和测试。
5. 不同时验证多个根因假设。
6. 不在证据不足时大规模重构。
7. 每完成一个节点就更新状态，避免最后一次性回忆。
8. 遇到模糊目标时先将其改写成验收条件，再编码。

## 持久化工程指令

当用户要让规则常驻 Codex、Copilot 或仓库时，读取 [instruction-layering.md](references/instruction-layering.md)。

使用五层结构，避免单文件过载：

1. 全局 Skill：通用工作协议
2. 根级 `AGENTS.md` 或仓库指令：项目不变量、命令和治理
3. 路径级指令：模块特有规范
4. `.agent-harness/` 状态文件：当前事实、决策、任务和交接
5. 单次任务卡：本轮目标、保护区、权限和验收

可运行 `scripts/init_project_harness.py` 安全生成项目状态模板。默认不覆盖已有文件；仅在显式使用 `--force` 时覆盖。使用 `--with-agents` 才创建根级 `AGENTS.md` 模板。

## 输出要求

根据任务规模自适应，默认使用以下紧凑结构：

- `MODE`
- `CURRENT REALITY`
- `TARGET / ACCEPTANCE`
- `DECISION`
- `PLAN` 或 `EXECUTION`
- `VERIFICATION`
- `RISKS`
- `HANDOFF / NEXT`

简单任务可压缩。需要严格模板时读取 [output-templates.md](references/output-templates.md)。

## 资源索引

- [operating-modes.md](references/operating-modes.md)：模式路由与各阶段检查表
- [planning.md](references/planning.md)：规格、方案比较、任务拆解和最小切片
- [implementation-debugging.md](references/implementation-debugging.md)：仓库侦察、编码与根因调试
- [verification-evidence.md](references/verification-evidence.md)：证据阶梯、完成层级和验收
- [retrospective-handoff.md](references/retrospective-handoff.md)：节点复盘、接力和恢复
- [instruction-layering.md](references/instruction-layering.md)：Skill、AGENTS.md、状态文件和任务卡分层
- [output-templates.md](references/output-templates.md)：规划、执行、调试、审查和交接输出模板
- [design-provenance.md](references/design-provenance.md)：设计来源与可迁移原则；仅在解释方法来源或更新本 Skill 时读取
