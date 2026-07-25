# KV Engineering Reasoning Harness

面向 Codex、ChatGPT、Claude Code、Cursor 等编码 Agent 的工程推理与接力增强 Skill，尤其适合能力较弱、上下文有限或需要跨会话接力的模型。

它通过明确的工作模式、事实纪律、证据阶梯和七级工程状态，把“请深入思考”转化为可执行的工程闭环：

> 核验现状 → 明确目标 → 选择路径 → 最小实现 → 分层验证 → 反方审查 → 状态交接

## 解决什么问题

- 项目开局时缺少完整侦察，直接开始写代码
- 接力开发时把旧总结当成事实，重复劳动或误伤已有修改
- 规划停留在“优化、完善、增强”等不可验收表达
- 调试时同时修改多个变量，无法确认真实根因
- 把代码修改、本地测试、提交、推送、PR、CI 和发布混成一句“已完成”
- 任务结束后没有可靠交接，下一位 Agent 只能重新调查

## 核心能力

- 八种工作模式：`INIT`、`RECOVERY`、`PLAN`、`IMPLEMENT`、`DEBUG`、`REVIEW`、`RETRO`、`HANDOFF`
- 五类事实状态：`OBSERVED`、`INFERRED`、`PLANNED`、`COMPLETED`、`BLOCKED`
- 七级工程状态：代码修改、本地验证、commit、push、PR、CI、release
- 分层验证与完成声明校准
- 项目保护区、兼容性不变量和最小完整切片
- 节点复盘、恢复旧项目和精确接力
- `AGENTS.md`、项目状态、任务卡、决策日志和交接模板
- 安全脚手架：默认不覆盖已有文件

## 目录结构

```text
kv-engineering-reasoning-harness/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── scripts/
│   └── init_project_harness.py
├── references/
│   ├── operating-modes.md
│   ├── planning.md
│   ├── implementation-debugging.md
│   ├── verification-evidence.md
│   ├── retrospective-handoff.md
│   ├── instruction-layering.md
│   ├── output-templates.md
│   └── design-provenance.md
└── assets/
    ├── icon.svg
    └── templates/
```

## 安装

### ChatGPT

下载仓库中的 `skill.zip`，在 ChatGPT 的 Skills 页面上传。

### Skill CLI

安装 `kv-skills` 仓库中的全部公开技能：

```bash
npx skillkit add Kvxw1105/kv-skills
```

单独安装本 Skill 时，优先下载本目录内的 `skill.zip`，或复制 `skills/kv-engineering-reasoning-harness/` 完整目录。

## 使用示例

```text
使用 $kv-engineering-reasoning-harness 接管当前仓库。
先核验分支、worktree、未提交修改、项目指令和关键调用链，
再选择工作模式，完成一个最小可验证闭环。
结束时分别报告代码修改、本地验证、commit、push、PR、CI 和 release 状态，
并生成下一位 Agent 可直接执行的交接。
```

```text
使用 $kv-engineering-reasoning-harness 对这个节点做复盘和下一阶段规划。
不要相信旧总结，先用 Git 状态、代码、测试和日志核验真实进度。
```

## 初始化项目接力文件

```bash
python scripts/init_project_harness.py /path/to/repository
```

同时创建根级 `AGENTS.md` 模板：

```bash
python scripts/init_project_harness.py /path/to/repository --with-agents
```

脚本会生成 `.agent-harness/` 下的：

- `PROJECT_STATE.md`
- `TASK_CARD.md`
- `HANDOFF.md`
- `DECISIONS.md`

已有文件默认保留。仅在明确需要覆盖时使用 `--force`。

## 设计原则

这套 Harness 不试图让弱模型凭空获得更高智力。它通过收紧自由度、保存关键事实、强制验证、限制改动半径和校准完成声明，让模型在工程任务中少犯低级但代价高昂的错误。

设计参考包括 Codex 的 `AGENTS.md` 分层指令、GitHub Spec Kit 的规格驱动工件链、Aider 的模式分离，以及 SWE-agent 的轨迹和复现思想。具体来源与迁移原则见 `references/design-provenance.md`。

## License

MIT
