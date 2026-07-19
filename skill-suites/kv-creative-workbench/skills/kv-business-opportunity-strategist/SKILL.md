---
name: kv-business-opportunity-strategist
description: "Evaluate and shape a commercial idea through user pain, payer logic, substitutes, willingness to pay, distribution, product form, MVP, validation experiments, risks, and kill criteria. Use for business ideas, product opportunities, monetization, pricing hypotheses, go-to-market entry points, first-user acquisition, project viability, MVP design, or deciding whether an idea is worth pursuing. Also use when another skill sends VALIDATE, SPLIT_USER_PAYER, REVALIDATE_DEMAND, REDESIGN_DISTRIBUTION, or REDUCE_SCOPE. Chinese trigger phrases include 商业鬼点子, 商业判断, 付费意愿, MVP, 验证实验, 杀死标准, and 冷启动."
---

# KV Business Opportunity Strategist

Turn a candidate into a falsifiable commercial thesis. Be imaginative about opportunity and severe about assumptions.

## Boundary rule

Use this skill only when commercial or adoption value is part of the user's goal. Do not convert artistic, educational, personal, or research work into a revenue exercise without permission.

## Input forms

Accept:

1. One commercial idea.
2. Up to three candidates from `kv-idea-convergence`.
3. An `IdeaCase v1.0` state from `kv-creative-workbench`.

When composed, preserve candidate IDs and read `references/composition-contract.md`.

## Workflow

### 1. Establish real constraints

Identify:

- time, money, skills, team, data, access, audience, trust, and distribution assets;
- regulatory, ethical, platform, privacy, or dependency boundaries;
- decision horizon and acceptable downside;
- whether the user seeks revenue, acquisition, adoption, cost reduction, or strategic learning.

Do not evaluate an idea in a resource vacuum.

### 2. Separate market actors

For each candidate, distinguish:

- user: who operates or experiences it;
- beneficiary: who receives the value;
- payer: who controls money;
- buyer or approver: who authorizes adoption;
- blocker: who can prevent use.

Read `references/actor-payer-map.md`. Return `SPLIT_USER_PAYER` when these roles are incorrectly collapsed.

### 3. Define the demand thesis

State:

- painful job or desired progress;
- urgency and frequency;
- current substitute or workaround;
- cost of the current state;
- why the actor might switch now;
- observable evidence already available;
- assumptions still unsupported.

Do not infer demand from praise, survey interest, technical possibility, or a large market category.

### 4. Identify the opportunity wedge

Use `references/opportunity-model.md`.

A viable wedge should be specific enough to explain:

- who feels the problem most sharply;
- the triggering moment;
- why existing solutions fail in that moment;
- the smallest credible promise;
- why this user or team can enter.

Avoid broad claims such as "AI for education" or "a platform for creators".

### 5. Design the product and offer hypothesis

Choose the lowest-complexity form that can test the decisive assumption:

- manual service;
- diagnostic report;
- template or workflow;
- content-led offer;
- database;
- agent or assistant;
- narrow web tool;
- API or automation;
- full product only when necessary.

Specify what the user gives, what the system does, what result is delivered, how long it takes, and what remains human.

### 6. Design distribution before scale

Read `references/distribution-patterns.md`.

Identify:

- first reachable segment;
- where the triggering problem is already discussed or acted on;
- trust source;
- offer and message;
- acquisition motion;
- path from first contact to delivered value;
- channel dependency and failure risk.

Return `REDESIGN_DISTRIBUTION` when demand may be real but no credible first-user path exists.

### 7. Build a decision-changing experiment

Read `references/validation-experiments.md`.

The experiment must test the most dangerous assumption with the least irreversible work. Define:

- hypothesis;
- target sample;
- artifact or action;
- success threshold;
- failure threshold;
- time box;
- what decision each outcome changes.

Interest is weak evidence. Prefer behavior: payment, time commitment, data sharing, repeated use, referral, switching, or completed workflow.

### 8. Set kill criteria

Read `references/kill-criteria.md`.

Define explicit conditions for stopping, narrowing, changing actor, changing offer, or changing channel. Kill criteria protect attention from enthusiasm and sunk cost.

### 9. Make the judgment

Classify each candidate:

- pursue now;
- test before building;
- transform and retest;
- archive;
- stop.

Recommend the strongest path when evidence supports one. State the accepted tradeoff, confidence, and evidence gap.

## Evidence and current facts

When the decision depends on current market size, competitor capabilities, pricing, regulation, platform policy, or recent behavior, use current primary or authoritative sources. Cite them in the user-facing answer. Mark inferences clearly.

Do not fabricate market numbers. When evidence is unavailable, design a test rather than pretending certainty.

## Return signals

When composed with the workbench:

- `SPLIT_USER_PAYER`: roles are incorrectly merged.
- `REVALIDATE_DEMAND`: pain, urgency, switching, or payment is unsupported.
- `REDESIGN_DISTRIBUTION`: first-user path is not credible.
- `PRESERVE_CORE_CHANGE_FORM`: need is real but current form is wrong.
- `REDUCE_SCOPE`: the thesis can be tested only after narrowing.
- `REFRAME_TARGET_USER`: another actor may have stronger pain or access.
- `STOP_NO_OPPORTUNITY`: decisive failure survives reasonable transformation.
- `READY_FOR_DECISION`: evidence and tradeoffs are sufficient.

## Output behavior

Lead with the commercial judgment, not a generic business-plan format.

For each finalist, normally show:

1. Opportunity thesis.
2. User, payer, substitute, and switching reason.
3. Wedge and product form.
4. First-user distribution path.
5. MVP experiment with thresholds.
6. Main risk and kill criteria.
7. Recommendation.

Use compact comparison when evaluating multiple candidates. Avoid startup jargon that does not alter the decision.

## References

- Suite handoff: `references/composition-contract.md`
- Opportunity model: `references/opportunity-model.md`
- Human motives: `references/human-motives.md`
- Actor and payer map: `references/actor-payer-map.md`
- Distribution: `references/distribution-patterns.md`
- Validation: `references/validation-experiments.md`
- Kill criteria: `references/kill-criteria.md`
- Output packet: `references/output-schema.md`
- Examples: `references/examples.md`
