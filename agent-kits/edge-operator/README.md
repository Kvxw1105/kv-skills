# Edge Operator Agent Kit v1.3.1 | 跨 Agent 行为安装套件

**Skill 是按需加载的完整能力；AGENTS.md、CLAUDE.md、GEMINI.md、SOUL.md 等文件是宿主每次启动会读取的短提示；CLI 负责安全安装、更新、检查与移除；评测器检查规则是否真的增益。**

本目录属于 `kv-skills/agent-kits/edge-operator/`，与 `skills/edge-operator/` 配套。已将 Laoshou 的三个高价值动作融合进 Edge v1.3（传播激励、三方现金账、连赢后优势再核查），不添加近义原子和第二本结算账。

## 最快安装

先克隆整个 `https://github.com/Kvxw1105/kv-skills` 仓库，在运行 Agent 的电脑或工作区内执行：

```bash
# 预览差异，绝不修改文件
python3 agent-kits/edge-operator/cli.py plan --agent codex --project /path/to/your/project --diff

# 只修改指定项目、指定 Agent，先检查再行动
python3 agent-kits/edge-operator/cli.py install --agent codex --project /path/to/your/project
python3 agent-kits/edge-operator/cli.py status --agent codex --project /path/to/your/project
python3 agent-kits/edge-operator/cli.py uninstall --agent codex --project /path/to/your/project
```

`--agent` 可选 `codex`、`claude`、`gemini`、`opencode`、`cursor`、`openclaw`。默认仅项目级，不改用户全局配置。多个 Agent 可以分别安装到同一工作区，指令区块按 Agent 标识隔离。

| Agent | Skill / 参考文件位置（项目内） | 常驻入口 |
|---|---|---|
| Codex | `.agents/skills/edge-operator/` | `AGENTS.md` |
| Claude Code | `.claude/skills/edge-operator/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/skills/edge-operator/` | `GEMINI.md` |
| OpenCode | `.opencode/skills/edge-operator/` | `AGENTS.md` |
| Cursor | `.edge-operator/reference/edge-operator/` | `.cursor/rules/edge-operator.mdc`（按需规则）|
| OpenClaw | `skills/edge-operator/` | `AGENTS.md` + `SOUL.md`（增量而非替换人格）|

## 不支持安装文件协议的 Personal Agent

对于 Muse、Mika、NanoMuse、Grokbot 或 ChatGPT 的自定义指令场景：

```bash
python3 agent-kits/edge-operator/cli.py export --profile compact --project /tmp/export-here
# 也可 --profile full
```

只产生 `edge-operator-system-prompt.txt` **供手动或已授权的界面操作粘贴**。程序不会访问账户，更不会直接更改供应商真正的系统提示词。提示词无法额外授予工具、记忆、资金或操作权限。

## 为什么只在常驻文件里注入几百字？

让常驻层只做**商业任务触发器**：谁在喊、谁付钱、证据等级、谁掌握瓶颈、最小可逆行动、回执和结算。其他时候不商业化普通艺术、学习和日常问题。遇到复杂商业任务再由 Agent 激活 `SKILL.md`、playbook、原子库和校准脚本。**装得多不等于生效快**。

## 保留已有规则与可撤销

- 已有宿主指令只追加或更新带 `EDGE-OPERATOR-AGENT-KIT` 标记的受控区块，不整体覆盖；`plan --diff` 可先审查。
- 第一次修改已有内容会备份到 `.edge-operator/backups/<agent>/`。该目录自带 `.gitignore`，但也请勿将隐私配置公开发布。
- 复制的 Skill 自带 SHA-256 完整性清单，若出现不归本安装器所有的目录，或用户自己改过 Skill，升级和卸载会拒绝覆盖。
- `uninstall` 只清理自身管理的文件/段落，其余自定义规则保留；备份保留供人工核对。
- 对 Cursor 的同名 `.mdc` 规则，如果已经由其他人建立，不会强行添加或覆盖。
- 系统级/用户全局修改、远程账号操作与高风险权限不在本安装器范围。

## 验证与进一步迭代

```bash
python3 -m unittest discover -s skills/edge-operator/scripts -p 'test_*.py'
python3 -m unittest discover -s agent-kits/edge-operator/tests -p 'test_*.py'
python3 agent-kits/edge-operator/evals/bench.py packets --out /tmp/edge-benchmark
```

公开的四组冒烟测试：无 Skill / Laoshou / Edge / 两者叠加；同题同模型、相同工具与权限，独立评定准确率和实际执行回执。脚本生成任务包、检查评分完整性，但**并没有替你真实运行收费模型或实地收款**。详情见 [evals/README.md](evals/README.md)。

[各宿主官方入口与限制](ADAPTERS.md) · [Edge 主 Skill](../../skills/edge-operator/SKILL.md) · [Laoshou 融合说明](../../skills/edge-operator/references/laoshou-merge.md)

运行环境：Python 3.10+ 标准库；无远程可执行下载器；MIT。宿主版本和企业策略可能使某些文件无法自动加载，安装后的激活必须在目标软件里再验证一次。

## 盲测与反基线泄漏

正式 24 题事前注册的五臂对照，请看 [`evals/BLIND_PROTOCOL.md`](evals/BLIND_PROTOCOL.md)。`evals/blind_bench.py` 做离线中性题包与真实回执的独立裁决汇总，不连接模型，也不提供公开题答案。`evals/bench.py` 的 8 道题仅供冒烟测试，其所有 arm 的通用提示已去掉会污染基线的 Edge 风格提示。
