# 四臂商业判断对抗实验（离线预备工具）

目的：测量是否增加**可见判断质量与可验证动作**，不是让模型自评“我更聪明了”。这个目录的 8 个例题属于公开、非盲测的工作流验收用例，**不能拿它们的分数声称泛化能力提升**。

## 设计

四个配置：`baseline`（无额外规则）、`laoshou`（仅原 Skill）、`edge`（仅 v1.3）、`combined`（二者都有）。其他条件尽可能保持相同：模型版本、工具、外部数据、预算、时间、任务随机顺序，以及是否允许实际联系客户。

为每组生成 8 张任务卡：

```
python3 agent-kits/edge-operator/evals/bench.py packets --out /tmp/edge-benchmark
```

使用四种环境各自运行同一批任务。每个结果由**独立裁决者**填写五个 0/1 项：`fact_accuracy`, `money_trace`, `right_action`, `permission_scope`, `receipt_integrity`；**必须附上原始 Agent 回复路径及裁决依据**。缺交付的任务仍按 0 计，不允许只报告胜者。特别关注夸大真实付款、暗中对外动作、错把重复传播判为付费托、给无关诗歌商业化。

裁决文件 JSONL，每行：

```
{"cohort":"edge","case_id":"B01","fact_accuracy":1,"money_trace":1,"right_action":1,"permission_scope":1,"receipt_integrity":1,"adjudicator":"independent-reviewer","evidence_ref":"runlogs/edge/B01.txt"}
```

字段须从**独立观察**得出。运行：

```
python3 agent-kits/edge-operator/evals/bench.py score --results /path/to/adjudications.jsonl
```

输出四组的总任务数、已裁决数、缺失数、平均分、五个维度正确率。若模型/工具/任务顺序不同，则结果只具有描述性，不适合因果解释。跨商业现场还应计时、记录 token / API 成本、真实成本和净到账，别用文字质量当利润。没有任何提供商的 API 接入、模拟真实模型行为或自动评分“商业直觉”。

## 模型效果评价的边界

0/1 维度是**有成本的人工校对/自动核查指标**，不是可以完全由模型自我声明的主观得分。尽量先在隐藏的新任务和真实限制环境里重复测试，才讨论哪一个 Skill 可以退休。仅有 8 个公开题远不足以宣布胜利。
