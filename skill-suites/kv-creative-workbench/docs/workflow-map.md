# Workflow map

## Stage ownership

| Stage | Owner | Exit condition |
|---|---|---|
| Intake | `kv-creative-workbench` | Goal, constraints, commercial requirement, and first unresolved bottleneck are known |
| Frame | `kv-language-ideation` | The problem statement opens a useful solution space |
| Diverge | `kv-language-ideation` | Candidate directions differ by mechanism, user experience, or causal structure |
| Converge | `kv-idea-convergence` | A defensible shortlist exists and weak forms have been transformed or rejected |
| Validate | `kv-business-opportunity-strategist` | Demand, payer, distribution, MVP, experiments, and kill criteria are explicit |
| Decide | `kv-creative-workbench` | Tradeoffs, recommendation, confidence, and next action are clear |

## Common routes

| Situation | Route |
|---|---|
| 模糊表达、常规答案过多 | Frame -> Diverge |
| 从模糊想法走到可测试方向 | Frame -> Diverge -> Converge -> optional Validate -> Decide |
| 已有大量点子 | Converge -> optional Validate -> Decide |
| 已有一个产品想法 | Validate -> Decide |
| 创意核好但形态过重 | Converge transform -> Validate |
| 需求存在但获客路径弱 | Validate distribution repair |
| 用户明确追求非商业目标 | Frame/Diverge/Converge -> Decide，跳过商业字段 |

## Rerun rule

Start at the earliest owner of a stale decisive field. Preserve unaffected evidence, candidate lineage, and rejection reasons. Resume downstream work only after the repaired field passes its gate.
