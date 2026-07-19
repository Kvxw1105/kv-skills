---
name: kv-idea-convergence
description: "Independently review, narrow, transform, and prioritize a set of ideas without losing valuable creative cores. Use when the user asks to select, compare, rank, filter, converge, critique, reduce many ideas, rescue an impractical concept, or choose what to pursue. Also use when another skill sends CONVERGE, PRESERVE_CORE_CHANGE_FORM, REDUCE_SCOPE, or a candidate packet. This skill performs blind review and should not inherit the generator hype or rankings. Chinese trigger phrases include 创意收敛, 筛选点子, 审查创意, 提取创意核, 改造方案, and 从多个方向里选择."
---

# KV Idea Convergence

Manage possibility after ideation. Preserve mechanisms worth keeping, remove fantasy shells, and deliver a small portfolio that fits the user's actual goal and constraints.

## Input forms

Accept:

1. A user-provided list of ideas.
2. A candidate packet from `kv-language-ideation`.
3. An `IdeaCase v1.0` state from `kv-creative-workbench`.

If the input contains persuasive descriptions, excitement scores, or generator rankings, normalize it before review. Read `references/blind-review.md`.

## Workflow

### 1. Confirm the decision context

Identify:

- real objective;
- commercial or noncommercial success criterion;
- time horizon;
- user resources and constraints;
- risk boundary;
- required portfolio size.

Use reasonable defaults when missing. Do not request context that cannot change the selection.

### 2. Build a blind review packet

For each candidate, retain only:

- ID and lineage;
- mechanism;
- target user or actor;
- use scenario;
- value created;
- dependencies;
- key assumptions;
- evidence level;
- resource burden.

Remove names temporarily when they create halo effects. Remove claims such as "revolutionary", "high potential", or "best" unless evidence supports them.

### 3. Classify before ranking

Assign each candidate to one primary class:

- Promote: worth immediate deeper work or a small test.
- Transform: valuable core, weak current form.
- Archive: meaningful concept, poor current timing or fit.
- Reject: weak core, weak fit, or fatal flaw.

Do not force every candidate into a numeric leaderboard. Read `references/evaluation-gates.md`.

### 4. Extract the creative core

For Transform and Archive candidates, identify:

- fantasy or costly shell;
- preserved mechanism;
- preserved user outcome;
- transferable pattern;
- lower-friction form.

Use `references/creative-core.md` and `references/transformation-patterns.md`.

### 5. Test decisive dimensions

Evaluate only dimensions that can change the decision:

- user and goal fit;
- mechanism distinctiveness;
- feasibility under current resources;
- value or use intensity;
- validation convenience;
- long-term asset potential;
- fatal legal, ethical, platform, data, or dependency risk.

Do not average away fatal flaws. Do not reject an original mechanism solely because its first form is expensive.

### 6. Construct the final portfolio

Default to two or three finalists:

- one option that can be tested quickly;
- one option with the strongest differentiated core, transformed if needed;
- optionally one strategic asset or longer-horizon option.

A portfolio must serve different roles. Do not return three minor variants.

### 7. Produce return signals

When composed with the workbench:

- `EXPAND_DIVERSITY`: candidate set is structurally homogeneous.
- `REFRAME_TARGET_USER`: mechanism has value but current actor fit is weak.
- `PRESERVE_CORE_CHANGE_FORM`: valuable core, invalid product or delivery form.
- `REDUCE_SCOPE`: concept can work only after narrowing.
- `STOP_NO_OPPORTUNITY`: no candidate survives and no meaningful core can be rescued.
- `READY_FOR_DECISION`: noncommercial decision is sufficiently supported.

Pass no more than three candidates to business validation unless the user asks otherwise.

## Decision discipline

Read `references/rejection-rules.md`.

Reject directly when a candidate has two or more unresolved fatal conditions such as:

- no identifiable user or beneficiary;
- no mechanism beyond branding;
- no validation path;
- resources far beyond the user's horizon;
- dependency on inaccessible data, permissions, or distribution;
- unacceptable legal or ethical risk;
- no fit with the user's stated objective.

Before rejecting a highly original candidate, perform one transformation attempt unless the fatal condition cannot be changed without destroying the core.

## Output behavior

Give the overall judgment first. For direct use, normally show:

1. Selection logic.
2. Promote, Transform, Archive, and Reject results.
3. Final portfolio and roles.
4. Strongest recommendation or unresolved tradeoff.
5. What should be tested or validated next.

Keep rejection explanations brief. Spend detail on finalists and transformations.

## References

- Suite handoff: `references/composition-contract.md`
- Blind review: `references/blind-review.md`
- Evaluation: `references/evaluation-gates.md`
- Creative core extraction: `references/creative-core.md`
- Transformation library: `references/transformation-patterns.md`
- Rejection logic: `references/rejection-rules.md`
- Output packet: `references/output-schema.md`
- Examples: `references/examples.md`
