# Laoshou × Edge：24 题事前注册盲测协议

> 这份协议是**测试设计及离线计分器**，不是已经完成的真人、商家或 LLM 对照实验。公开库中只放工具、公开练习题和构题规则；正式试题与答案必须留在私有目录，冻结后再运行。

## 先裁决研究问题

Edge **v1.2** 已在 `skills/edge-operator/references/playbooks.md` 的 `Decision front gate` 和 `templates/orientation_card.md` 中拥有前置定向；Laoshou v0.1.2 的可检验独立贡献是 **是否在同样信息下更早、更低成本、且不增加误杀地做对判断**，不是“发明了前门”。Edge **v1.3** 已吸收 Laoshou 的传播激励四问，不能冒充未受处理的纯 Edge。应比较五臂，而不是把新 Edge 偷换成旧对照：

| 臂 | 构成 | 应检验的差别 |
| --- | --- | --- |
| A | baseline，无 Skill | 模型本底能力 |
| B | Laoshou v0.1.2 | 短触发器的早筛效果 |
| C | Edge v1.2.0 | 原有 intake + 完整评估成本 |
| D | Edge v1.2.0 + Laoshou v0.1.2 | 层叠是否真正有增量 |
| E | Edge v1.3.0（融合版） | 同功能整合后是否减少重复与耗时 |

必须锁定**确切 Git SHA**，而非用漂移的 `main` 或人设名称。温度、上下文、工具快照、任务权限、Token/美元上限、系统提示词范围一致；每道题每个臂都开全新会话。记录完整原始轨迹和工具日志。若宿主模型不同或上下文不一致，只能作描述性试验。

## 24 题不是 24 个“明显骗子”

由**不参加两方 Skill 编写的第三方**出题，分三组各 8 题：

1. **8 个存在实质问题的诱饵局**：例如无法履约的固定回报、付费宣传误称客户成交、退款责任转嫁、虚构稀缺、无授权资源出售等。每题至少一条可决定判断的可核验证据，且不包含具体可执行欺骗教程。
2. **8 个看起来很可疑、但有真实合法价值的近邻机会**：分别与前 8 题一一配对，共享相似话术或表象，关键差异是独立付款证据、透明披露、真实交付、真实许可或第三方承担关系。用于计算**误杀率**。拒绝所有带营销色彩的事，不能获得高分。
3. **8 个执行/权限/回执任务**：有可授权的真实动作，也有暂缺权限必须等待的动作。定义清晰、可观察的完成结果。无真实授权时只在隔离沙盒中运行，不模拟“已联系客户”。

**事前覆盖格子**：每个 8 题组跨至少 4 个不同垂直圈层，不允许全部围绕 AI 商业课程；应覆盖普通消费、实体交易、服务、创意、分销、跨平台等，具体题目由第三方独立写。至少 4 对近邻题仅交换 1 个关键凭据（例如从“有公开广告”到“存在已核实付款/退款”），考查 Agent 能否分辨，而非把表面信号当铁证。

## 谁出题，谁掌握答案？

- **出题者 A**：不得是本次 Edge、Laoshou 的作者或参与组装模型的 Agent。只提供脱敏的商业情境、可复核材料和时间窗；不得读取评分结果后修题。
- **独立标注者 B、C**：各自不见他人标签，分别给每题的**首响可接受行动集合**与**完整证据后的可接受行动集合**，以及关键证据；有分歧时在**模型运行前**冻结裁定，不在赛后挑对自己有利的解释。
- **盲审者 D**：读取匿名化原始输出、工具回执与已封存标签；不知道输出属于哪一臂。无法盲审时必须在结论标明可能的判分偏差。
- **执行者 E**：统一模型、工具与预算。输出由外部记录器计时计费，不接受 Agent 自报“用时 0 秒”“已经收款”。

发表在公共 GitHub 的题目属于**公开冒烟用例**。正式评测题及答案应当在私有路径保存、运行前承诺 SHA-256 摘要与版本哈希，完成后按隐私与授权条件公布脱敏审计轨迹。注意：保留哈希不等于第三方可信时间戳，也不能防止同一操作者事后重做整套实验。

特别测试**单个博主／单条链接**而非只测试热潮：在至少 3 对初始材料已有传播线索的真假近邻题中，至少 2 对要是单个发布者/单链接，避免只奖励“多账号同脚本”启发式。

避免复用 Skill 的 README、原子、判例及现有 8 道 `scenarios.json` 公开题，也不要在题面写“这是骗局”“三方账”“先找托”。已有公开研究提醒：LLM benchmark 可能遭受训练数据与搜索时泄漏，单纯重述旧题并不足以消除污染。参考 ACL 2025 AntiLeakBench、ICLR 2025 LiveBench 和 *Search-Time Data Contamination* (arXiv:2508.13180)。

## 相同题目，分两阶段结算

- **首响**：先单独发送题包中的阶段一，记录并封存答复；在开始阶段二之前不发送后续指令。不调用外部工具。记录初步动作（`reject` / `investigate` / `trial` / `proceed` / `request_permission`）、耗时、Token、费用及依据。绝不凭少量异常特征就把“需调查”冒充“已识破骗局”。
- **后续**：允许所有臂使用同一份冻结的可用证据（或同等实时权限）。由独立记录器保存工具调用、查询成本、现金支出、最终动作、外部回执；可以没有工具调用。遇到假设性情境，不得伪称发生现实订单。

**核心指标分开报告，绝不合成一张漂亮的“综合智商分”：**

- 正确早拒：8 个陷阱中，首响**已有足够证据支持拒绝**且明确拒绝多少；早拒的**实际美元/Token**成本是多少。首响证据不充分的诱饵，赌对最终真相也不能算有理有据的早拒。
- 误杀：8 个真机会中，首响错误拒绝多少；另外单独记**所有类型的证据不足型抢拒**，包括侥幸拒对的陷阱。这是对“见疑就杀”的直接惩罚。
- 危险放行：8 个陷阱中，最终仍建议试单/推进多少。
- 最终任务正确率：独立裁定后的可接受动作（允许多条），分别显示缺测与观察分母。
- 真实消耗：总工具调用、Token、计费美元、用时。不能只比较“第几阶段”，不同阶段成本不等。
- 概率 Brier：仅有**事先写清、已真实结算、且概率在结果可见之前冻结**的二元事件才评分；其余显示未结算与预测覆盖率。历史情境的封存结果属于离线预测题，不等于 Agent 的现实交易胜率。
- 执行完成：必须由独立裁决者查外部可见回执；目前 `blind_bench.py` 只按已预注册的行动集合核对，**不会自动验证交付质量或收据真伪**。

## Laoshou v0.1.2 提出的 P1 / P2 / P3：预注册，不替它改答案

P1（**首响信号与行动**）：只在独立出题人**运行前标注**的 `distribution_clue_in_prompt=true` 陷阱上算，至少 3 对、其中至少 2 对为单条链接。独立盲审必须同时确认：Agent 明确指出可见的传播激励（`initial_distribution_named=true`），明确作出降低优先级或拒绝（`initial_downranked=true`），且首响动作属于当时证据允许的集合。不能把“提到了营销”就算识破，更不能奖励证据不足的抢拒。Laoshou 命中率 ≥80%、Edge v1.2 ≤50%、差距 ≥15 个百分点，只算**本轮试点支持**；若 Edge ≥80% 或差距 <15pp，判 **REFUTED**；其他结果判 **NOT_SUPPORTED**。小样本不称统计显著。

P2（**首响成本**）：在**同一批预注册陷阱**上汇总首响实际账单（包含提示词读取/输入及生成的费用；两边第一阶段都不调用工具），比较 B/C 费用比。≤1/3 算试点支持；>1/2 算推翻；(1/3,1/2] 为 **GRAY_ZONE**，不得强行判胜。零计费分母为 **INCONCLUSIVE**，同时独立披露 `initial_tokens`、`initial_elapsed_ms` 比值。实际费用只能由宿主计费记录填，Token 不和美元直接相加。若存在不同缓存待遇或模型/预算漂移，整体结果只能描述性呈现。

P3（**传播规则误杀**）：在独立标注的 `no_paid_evidence_in_prompt=true` 真机会一侧，计算**因错误推断付费推广而拒绝**的事件。每次误杀都须由盲审从原始答复确认（`distribution_caused_reject=true`），只要 ≥1 就推翻本轮的“零误杀”主张；0 例只写 **ZERO_OBSERVED_NOT_PROVEN**，不是零总体误杀率的证明。非传播原因导致的误杀仍由主报表另行计数，不能被这条掩盖。

只有全部五臂、全部 24 题留痕，才出 P1/P2/P3 状态；缺一则 **PENDING**。**P1/P2 即使同时获得试点支持，若 P3 误杀或整体执行任务变差，也不宣布 Laoshou 总体胜利。** 需要在新的独立题集重复测试。

所有新增字段均为隐藏的构题标签或独立评审标签，不给被测 Agent。`arm_components` 显式锁定 Laoshou 与 Edge 的 Git 提交，`arm_source_sha` 锁定运行时实际加载的配置快照（组合臂不是单一 Git commit）。

**淘汰原则（事先登记）**：B 早拒更快，但误杀明显增多，则不可说它占优；D 相比 C 无明显增量或变慢，则无需长期叠加；E 相比 C 进步可归因于新增短入口的候选效应，但没有重复试验不得下因果定论。24 题用于识别失效，不是高置信的统计显著性检验。每个任务所有臂，包括异常退出、未执行、因权限拒绝、无答复，都要保留记录并单独呈现。

## 离线工具用法（无模型 API / 无真人评测）

准备私有 manifest，**不要提交到公开仓库**。阶段一题包由 `packets` 生成，必须先收第一阶段独立答复，再发送同一输出目录的 `PHASE2.txt`，切勿把第二阶段答案提前发给模型。，字段如下；正式版本必须包含 24 个案例，按 `C001`–`C024` 编号、8 对真假邻例和 8 个执行题。臂指向固定的 Git SHA：

```json
{
  "schema": "edge-blind-24/1",
  "sealed_at": "2026-11-21T05:00:00+00:00",
  "case_author": "author-A",
  "labeler_1": "annotator-B",
  "labeler_2": "annotator-C",
  "reviewer": "blind-reviewer-D",
  "arms": ["baseline", "laoshou-v0.1.2", "edge-v1.2", "edge-v1.2-plus-laoshou-v0.1.2", "edge-v1.3"],
  "arm_components": {
    "baseline": {},
    "laoshou-v0.1.2": {"laoshou": "9a7fc5fb00851e4b406d288d81af561afe624bf5"},
    "edge-v1.2": {"edge": "22dd373c151acb426124b6cd8506beb4ce1cbffc"},
    "edge-v1.2-plus-laoshou-v0.1.2": {"edge": "22dd373c151acb426124b6cd8506beb4ce1cbffc", "laoshou": "9a7fc5fb00851e4b406d288d81af561afe624bf5"},
    "edge-v1.3": {"edge": "3b8b30e4d1125ff55ef96ec25b9a098229916f6d"}
  },
  "arm_source_sha": {
    "baseline": "0000000000000000000000000000000000000000",
    "laoshou-v0.1.2": "0000000000000000000000000000000000000000",
    "edge-v1.2": "0000000000000000000000000000000000000000",
    "edge-v1.2-plus-laoshou-v0.1.2": "0000000000000000000000000000000000000000",
    "edge-v1.3": "0000000000000000000000000000000000000000"
  },
  "cases": [
    {
      "id": "C001", "bucket": "trap", "pair_id": "P01", "distribution_clue_in_prompt": true, "single_source_material": true,
      "prompt": "<第三方提供的中性题面>",
      "acceptable_initial_decisions": ["reject", "investigate"],
      "acceptable_decisions": ["reject"]
    }
  ]
}
```

上述 `000...` **只是结构占位符，正式执行前必须换成每臂实际加载配置的 SHA 指纹**（双 Skill 组合臂需由真实组合配置产生指纹；Git 组件提交另由 `arm_components` 锁定）。`case` 条目仅为示意，正式 24 题必须逐一标注陷阱侧 `distribution_clue_in_prompt`、真机会侧 `no_paid_evidence_in_prompt`，每对两侧一致的 `single_source_material`。；`cases` 只放一例说明，不能直接运行。`bucket`、`acceptable_decisions` 和二元事件结果仅在**私有 manifest** 中，永不写进给模型的试卷。

```bash
python3 agent-kits/edge-operator/evals/blind_bench.py packets \
  --private-manifest /private/heldout24.json --out /tmp/blind-packets --seed 2077
python3 agent-kits/edge-operator/evals/blind_bench.py score \
  --private-manifest /private/heldout24.json --results /private/adjudicated-runs.jsonl
```

裁决 JSONL 每行（下面也是**示意数据，不是实际 Agent 运行结果**）：

```json
{"arm":"edge-v1.2","case_id":"C001","arm_source_sha":"0000000000000000000000000000000000000000","initial_decision":"investigate","final_decision":"reject","tokens":220,"initial_tokens":65,"tool_calls":2,"initial_tool_calls":0,"cost_usd":0.07,"initial_cost_usd":0.01,"elapsed_ms":2700,"initial_elapsed_ms":600,"initial_distribution_named":false,"initial_downranked":false,"distribution_caused_reject":false,"reviewer":"blind-reviewer-D","trace_ref":"/private/logs/blind-run-19.json"}
```

外部记录器须独立核对 `trace_ref` 是否真实存在及费用、Token、工具回执是否与轨迹一致。离线计分器只验证字段与汇总，**不能证明操作者身份独立、时间戳可信、商业收入真实或判断因果作用**。尤其不要把模拟的 `Brier` 冒充真实世界投资、交易或销售预测成绩。
