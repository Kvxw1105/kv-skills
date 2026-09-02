# kp-chatgpt-web-orchestrator · ChatGPT Web 总调度

> **A Harness-agnostic controller protocol for using signed-in ChatGPT Web as a supervised second execution engine.**
>
> 让 Codex、ZCode、Claude Code 或其他具备浏览器能力的 Agent 调度网页端完成研究、Skill、连接器和文件任务，并持续验收与落盘。

## What it is

这个 Skill 解决的不是“如何自动点击 ChatGPT”，而是更上层的问题：什么时候值得把工作交给网页端、怎样形成完整工作包、如何低成本等待与读取、如何纠偏续跑，以及怎样把网页回答变成经过验证的持久资产。

Skill 本身不绑定某个 Harness。目标 Agent 只需具备等价的浏览器控制、文件读写和状态持久化能力；没有内置浏览器时，可以接入标准 MCP 浏览器桥。

## Core capabilities

| Layer | What it does |
|---|---|
| Routing | 判断任务由控制 Agent、ChatGPT Web 或双方并行完成 |
| Delegation | 生成带目标、约束、验收和交付物的结构化任务单 |
| Supervision | 低频等待、精确续跑、上下文饱和后换会话接力 |
| Verification | 把网页输出视为候选，验证来源、文件、代码和真实行为 |
| Portability | 通过浏览器适配契约支持原生浏览器、MCP Bridge 或 Playwright |

## Usage

```text
$kp-chatgpt-web-orchestrator
Use my signed-in ChatGPT Web for the research and document-generation portions of this task. Keep ownership of the final goal, verify the result, and save useful artifacts locally.
```

## Install

```bash
npx skillkit add Kvxw1105/kv-skills
npx skills add Kvxw1105/kv-skills
```

Then select `kp-chatgpt-web-orchestrator` from the installed skills.

## License

MIT
