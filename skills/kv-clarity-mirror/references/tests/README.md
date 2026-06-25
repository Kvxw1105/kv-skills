# Test Scenarios for Blind Spot Mirror

> TDD for Skills：先定义"失败长什么样"，然后验证 skill 能否 catch 住它。

## 测试方法论

这些测试场景借鉴了 Superpowers 的"TDD for Skills"理念。每个场景的结构是：

1. **Setup**：描述一个具体的任务场景
2. **Expected Failure**：如果没有 blind-spot-mirror，AI 最可能犯什么错
3. **Expected Catch**：加载 blind-spot-mirror 后，`Runtime triage` 应该定位到哪个风险，应该采取哪个修正动作
4. **Pass Criteria**：怎么判断 blind-spot-mirror 在这个场景中"工作了"

## 怎么使用这些测试

**方法 1：手动测试**
1. 选一个场景
2. 不加载 blind-spot-mirror，让 AI 执行场景中的任务
3. 观察 AI 是否犯了 Expected Failure 中描述的错
4. 加载 blind-spot-mirror，让 AI 重新执行同一个任务
5. 观察 AI 是否用 Runtime triage 定位了 Expected Catch 中描述的风险，并采取对应修正动作
6. 用 Pass Criteria 判断结果

**方法 2：自我测试**
1. 加载 blind-spot-mirror
2. 读一个场景的 Setup 部分
3. 在脑中模拟你会怎么回应
4. 对照 Expected Failure 检查你是否会犯那个错
5. 对照 Expected Catch 检查你是否会触发那个检查

## 场景目录

### Fake Completion
- `fake-completion/scenario-fabricated-numbers.md` — 编造数字的场景
- `fake-completion/scenario-untested-code.md` — 未测试代码的场景
- `fake-completion/scenario-confident-outdated-info.md` — 自信地给出过期信息

### Execution Gap
- `execution-gap/scenario-advice-not-action.md` — 给建议而不是执行
- `execution-gap/scenario-todo-placeholder.md` — 代码中留 TODO
- `execution-gap/scenario-tool-available-but-unused.md` — 有工具不用

### Sycophancy
- `sycophancy/scenario-wrong-premise.md` — 用户前提有误
- `sycophancy/scenario-bad-tech-choice.md` — 用户选了不合适的技术

### Chains
- `chains/scenario-confidence-cascade.md` — 自信级联链
- `chains/scenario-helpfulness-trap.md` — 好心办坏事链
