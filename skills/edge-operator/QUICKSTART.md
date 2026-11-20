# Edge Operator v1.0 · 启动与跨 Agent 移植

## 目的

把**产品、交易、骇客、灰产分析、心理学、博弈、传播、执行**的思维变成可复用的商业行动协议。96 枚思维原子、64 个角色原型、16 个混合组合、7 条实战工作流、8 份跨平台提示词、权限模板、任务合同和简单的单位经济脚本。

它不会自动接管账号、安装插件、替用户付款或创造工具。每个 Agent 的实际能力和授权需要独立核实。

## 立即用

**ChatGPT Skills 环境**：上传 `skill.zip` 中的单个 `edge-operator` Skill，按平台的 Skill 安装流程启用。创建 ZIP 不代表已经安装成功。

**不支持 Skills 的 Muse、Grokbot、DSH、Codex、Mika、NanoMuse 等**：复制 `prompts/MASTER_PROMPT.txt` 到其长期指令/系统角色配置（如果有），上下文特别紧张时使用 `prompts/QUICK_START.txt`，再追加对应专职提示词；任务级别输入要附具体目标、可用工具和授权。各平台支持的“长期指令”不一定一致。

**要让不同 Agent 互认任务而非幻想互通**：给主控使用 `prompts/ORCHESTRATOR.txt`，把 `templates/mission.json` 改为真实任务合同，代理按 `templates/task_handoff.md` 回执。优先存入一个实际共享且授权的工作区。

## 示例唤醒

- “用钱迹猎人 + 灰转白，调查这个看起来靠规则漏洞赚钱的领域，给我一个能合法卖的结果，并说明谁现在真的付款。”
- “用技术换钱组合：这个开源手机 Agent 能帮普通消费者处理什么已在付费的任务？做出样品和报价模型。”
- “我的账号不要做假专家。用 IP 建国组合，找到能长期公开负责的观点，并生产一条有真实来源的内容。”
- “给云端研究、手机操作和本地开发 Agent 派一轮有回执的任务，不要编造已经连通。”
- “只做一个动作：把这个具体想法变成今天能验收的样品，按最短路径执行。”

## 配置与验收

1. 根据真实工具和授权编辑 `templates/permission_charter.yaml`。
2. 每次新任务编辑 `templates/mission.json` 或用同等结构创建任务。
3. Python 可用时运行 `python scripts/validate_mission.py templates/mission.json`。
4. 有明确假设数据时运行 `python scripts/unit_economics.py templates/example_deal.json --json`。
5. 为了避免装神棍，任何关键收入判断都要分清报价、净到款、贡献、复购与失败。
6. 使用 `references/evaluation.md` 的 12 个红队场景测试各模型是否实际遵循指令。跨模型能力不保证等同。

## 如何与已有 Skills 配合

- `ambition-engine`：对开放任务做有价值的上限探索。
- `consumer-demand-arbitrage`：从圈外用户正在付的钱倒推产品。
- `edge-operator`：将以上发现转化成角色选择、钱流分析、执行合同、跨代理协作与可验收结果。

三者是分工，不是简单叠加三份长提示词；若上下文有限，优先本 Skill 的 `SKILL.md` 与最相关的两份 reference。

### 研究/商机模式 v1.1

读取 `references/research-synthesis-2026-11-20.md` 与 `prompts/EVIDENCE_FIRST_OPERATOR.txt`，对机会卡运行 `python scripts/evidence_gate.py examples/etsy-authenticity-2026/opportunity-evidence.json --json`，别将报价、抱怨、模拟收益当成实付。
