# Agent 提示词编译协议

## 输入变量

至少提供：项目名称、类型、核心用户、核心任务、技术栈、当前问题、目标气质、必须保留、禁止改动、交付形式和可用工具。

## 模型分级

### 强 Agent

可一次读取仓库、执行命令、改多文件、运行浏览器和测试。使用 `full` 或 `existing-project` profile，但仍要求先建立保护边界和增量交付。

### 中等 Agent

拆为四轮：审计冻结 → Token/Showcase → 动效/创意层 → 扩散/验收。每轮只改变一个层级。

### 弱模型

拆为六轮：只读现状 → 只做视觉基线 → 只做一个 Showcase → 只修共享组件 → 只做适配性能 → 只做回归。提供明确正反例、文件范围和验收标准，不让其自由混合风格。

## Prompt 结构

1. 角色与唯一目标；
2. 真实项目输入；
3. 功能冻结和禁止改动；
4. 本轮范围；
5. 视觉/交互/工程合同；
6. 文件级实施顺序；
7. 测试与证据；
8. 输出 Schema；
9. 未验证与回滚。

## 编译器

```bash
python scripts/compile_prompt.py --profile workspace --project "Video Workbench" --set PROJECT_TYPE="创作工作台" --set MUST_KEEP="API、路由、时间线数据" --out prompt.md
```

`--modules` 可覆盖 profile。模块内容位于 `prompt-modules/`，只组合当前任务需要的能力，避免上下文膨胀。
