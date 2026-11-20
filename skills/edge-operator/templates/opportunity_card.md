# 交易机会卡（替换所有方括号）

- 机会名称：[一句不装腔的名称]
- 谁付钱：[付款方与支付触发，未知则写未知]
- 用户眼中的结果：[可见的交付物，而非技术功能]
- 现成替代：[竞品/人工/自己做及其代价]
- 钱正流向谁：[商家、渠道、平台、抽成关系]
- 真实观察：[链接/日期/原话/样本量/证据等级]
- 可进入的缺口：[具体抱怨、失败链路或价格/服务差]
- 我们真正能做的：[已掌握能力与尚缺资源]
- 试探报价：[金额、币种、来源或假设标注]
- 履约与成本：[工具/API/人工/支付/退货/获客]
- 假设订单贡献：[仅在有足够数据时计算，明确情景]
- 风险与授权：[法律/规则/隐私/第三方/账号]
- 下一步可观察动作：[负责人、动作、验收证据、止损]
- 当前状态：[IDEA | EVIDENCE | DEMO | QUOTED | PAID | REPEAT]

**注**：曝光、咨询、报价、订金、实付、净回款、复购不能混同。无公开价格或交易凭证，不得称“已证实有人为该服务付费”。

## v1.2 Required decision overlay (only when selecting/acting on an opportunity)

- **Forecast event definition / cohort / threshold**: [exact binary observation; not just "market works"]
- **Numeric probability p**: [0..1 estimate or remain DRAFT if cannot honestly define event]
- **Falsification metric**: [observable, including what counts as evidence AGAINST]
- **Settlement date**: [YYYY-MM-DD, receipt and reviewer]
- **Outside-view reference class**: [numerator / denominator / date / URL / selection bias, or UNKNOWN]
- **Competing explanations**: [>=2, strongest disconfirming test for each]
- **Position and bypass**: [bottleneck owner, who can charge, can client bypass us?]
- **Decay trigger and recheck date**: [why gap persists and what erases it]
- **Relevant atom IDs and evidence tiers**: [check references/atom-registry.json]
- **Human touchpoint**: [one short direction packet and one settlement packet, not unnecessary approvals]
- **Frozen forecast file/id/hash**: [link to append-only or Git-committed snapshot; never invent]

See `templates/orientation_card.md` and `templates/forecast_example.json`. Source caveats, net cash and external execution receipts still apply. Brier without a comparable settled sample is descriptive only.
