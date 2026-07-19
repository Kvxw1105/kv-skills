# Routing protocol

## Stage ownership

| Stage | Primary owner | Purpose |
|---|---|---|
| Intake | Workbench | Determine objective, route, constraints, and defaults |
| Frame | kv-language-ideation | Expose restrictive wording and create stronger questions |
| Diverge | kv-language-ideation | Generate candidates with different mechanisms |
| Converge | kv-idea-convergence | Blind-review, classify, transform, and narrow |
| Validate | kv-business-opportunity-strategist | Test demand, payer, distribution, MVP, and kill criteria |
| Decide | Workbench | Resolve tradeoffs and define the next action |

## Route selection

1. Ask whether the user lacks a direction, has many directions, or has one direction.
2. Ask whether the requested success criterion is commercial.
3. Identify the first unresolved bottleneck.
4. Start at the bottleneck, not at the beginning of the pipeline.
5. Stop when the requested outcome is achieved.

## Route table

| Situation | Route |
|---|---|
| Fuzzy phrase, conventional answers | Frame -> Diverge |
| Need end-to-end direction | Frame -> Diverge -> Converge -> Validate -> Decide |
| Many existing ideas | Converge -> optional Validate -> Decide |
| One product idea | Validate -> Decide |
| Strong idea, too expensive | Converge transform -> Validate |
| Real demand, weak acquisition | Validate distribution repair |
| All candidates feel similar | Return to Diverge with `EXPAND_DIVERSITY` |
| User rejects business framing | Mark `commercial_required: false`; redefine success and skip Validate |

## Activation ledger

Maintain internally:

| Skill | Role | Action performed | Contribution used | Retained |
|---|---|---|---|---|

Only count a specialist as activated after loading and applying its instructions.
