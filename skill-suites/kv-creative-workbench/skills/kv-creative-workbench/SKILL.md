---
name: kv-creative-workbench
description: "Orchestrate an end-to-end creative decision workflow from a vague idea to a framed, narrowed, validated, and actionable direction. Use for complex ideation, product concepts, content or IP directions, business ideas, project selection, idea repair, or any request that needs two or more stages including reframing, divergence, convergence, opportunity validation, MVP design, or decision. Also use when the user mentions a creative workbench, a combined idea workflow, linked skills, or asks to turn a fuzzy thought into a testable plan. Chinese trigger phrases include 创意工作台, 商业创意, 鬼点子, 先发散再收敛, 从模糊想法到验证, and 流程化组合调用."
---

# KV Creative Workbench

Operate as the control plane for a creative decision system. Route work across specialized skills, maintain one shared IdeaCase, and rerun only the fields invalidated by new information.

## Core operating rule

Do not run every stage by habit. Diagnose the user's current bottleneck, choose the smallest sufficient route, and preserve useful work across revisions.

Use these specialist skills when they are available:

- `kv-language-ideation`: reframe language and generate heterogeneous candidates.
- `kv-idea-convergence`: blind-review, classify, transform, and narrow candidates.
- `kv-business-opportunity-strategist`: test demand, payer logic, distribution, MVP, experiments, and kill criteria.

When the runtime supports skill discovery, actually read and execute the selected specialist entrypoints. Do not claim a skill was activated unless its instructions were loaded and used. If a specialist is unavailable, use `references/fallback-protocols.md` and disclose the fallback only when it materially affects quality.

## Workflow

### 1. Establish the real objective

Identify:

- what decision or artifact the user needs;
- whether the goal is commercial, noncommercial, or mixed;
- the time horizon;
- decisive resources, constraints, and risk boundaries;
- what already exists and should be preserved.

Do not force business analysis onto an artistic, educational, personal, or research goal. If information is missing but a reasonable default permits progress, state the assumption briefly and continue.

### 2. Create or update one IdeaCase

Use the canonical schema in `references/idea-case-schema.md`.

Maintain candidate lineage with stable IDs:

- New candidate: `I-01`, `I-02`, and so on.
- Transformed child: `I-03A`, `I-03B`.
- Never silently replace a candidate. Record what was preserved and what changed.

Keep the full state internal unless the user asks for the process, a reusable report, or a machine-readable handoff. In normal answers, expose only the parts that help the user decide.

### 3. Select a route

Read `references/runtime-modes.md` and `references/routing-protocol.md`.

Default routes:

- Fuzzy problem or ordinary ideas: Frame -> Diverge -> Converge -> Validate if commercial -> Decide.
- Existing candidate list: Converge -> Validate if commercial -> Decide.
- One mature idea: Validate -> Decide; return upstream only if a core assumption fails.
- User wants only brainstorming: Frame -> Diverge and stop.
- User wants only selection: Converge and stop.
- Existing plan failed: Diagnose the failure and return to the owning stage.

### 4. Run specialists with clean handoffs

Before convergence, remove generator hype, self-rankings, and persuasive adjectives. Pass mechanisms, assumptions, users, scenarios, constraints, and dependencies. This creates a blind-review boundary.

Before business validation, pass no more than the strongest three candidates unless the user explicitly requests a wider portfolio. Preserve one immediately testable option and, when justified, one high-originality option that requires transformation.

### 5. Process return signals

Use only the signals in `references/return-signals.md`.

A return signal must specify:

- the failed assumption;
- the stage that owns the repair;
- fields to preserve;
- fields to invalidate;
- the minimum rerun required.

Limit the automatic loop to three passes. After that, present the unresolved tradeoff or evidence gap instead of cycling indefinitely.

### 6. Invalidate dependencies, not the whole case

Read `references/dependency-graph.md`.

When the user changes a condition, mark affected fields stale and rerun only those fields. Examples:

- Changing target user invalidates fit, ranking, payer, distribution, and validation; it need not erase the core mechanism.
- Changing budget invalidates feasibility, product form, MVP, and test design; it need not erase framing.
- Changing the goal from commercial to artistic skips pricing and payer logic and reevaluates success criteria.

### 7. Pass quality gates

Read `references/quality-gates.md`.

Do not deliver a final recommendation until:

- the real objective is explicit;
- candidates differ by mechanism, not only wording;
- convergence was independent of generator enthusiasm;
- commercial conclusions identify user, payer, substitute, acquisition path, experiment, and kill condition;
- assumptions and unknowns are visible;
- the next action is concrete and reversible where possible.

## Routing priorities

Use this order when instructions conflict:

1. User's real goal and explicit exclusions.
2. Facts, legal and safety boundaries, and current evidence.
3. Causal coherence and feasibility.
4. Originality and expression.
5. Output polish.

Do not let a creative metaphor alter a factual conclusion. Do not let business attractiveness erase a noncommercial objective.

## Output behavior

Give the key judgment first. Adapt the visible structure to the request rather than dumping the full pipeline.

For a standard end-to-end result, usually show:

1. Reframed opportunity or problem.
2. Final candidate portfolio, normally two or three options.
3. Decisive tradeoffs and why one option leads.
4. Validation action or next move.
5. Assumptions, risks, and stop conditions.

If the user asks how the system worked, provide a compact activation ledger with each specialist's role, action, and contribution. Do not reveal private chain-of-thought.

## References

- Canonical state: `references/idea-case-schema.md`
- Routing: `references/routing-protocol.md`
- Runtime modes: `references/runtime-modes.md`
- Return signals: `references/return-signals.md`
- Dependency invalidation: `references/dependency-graph.md`
- Quality gates: `references/quality-gates.md`
- Specialist fallback: `references/fallback-protocols.md`
- Worked cases: `references/examples.md`
