---
name: kv-language-ideation
description: "Reframe restrictive language and generate genuinely different creative directions before feasibility analysis. Use for brainstorming, concept creation, naming systems, content or product ideation, research-question reframing, non-obvious angles, creative blocks, or requests to open the problem space. Also use when another skill sends FRAME, DIVERGE, REFRAME_ROOT, EXPAND_DIVERSITY, or REFRAME_TARGET_USER. Do not use as the primary skill when the user only needs commercial validation or final prioritization. Chinese trigger phrases include 创意发散, 语言框架, 重构问题, 打开脑洞, 重新命名, and 语言造境."
---

# KV Language Ideation

Change the question before multiplying answers. Analyze how the user's words constrain the solution space, then generate candidates that differ by mechanism rather than decoration.

## Operating modes

Choose one mode from `references/modes.md`:

- Standard: calm, clear reframing and usable divergence.
- Breakthrough: stronger metaphors, opposites, boundary shifts, and language games.
- Dual-pass: breakthrough expansion followed by de-dramatization and cleanup.

Default to Standard. Use Dual-pass when the user asks for a major creative leap or previous ideas are conventional.

## Input forms

Accept either:

1. A direct user request or fuzzy idea.
2. An `IdeaCase v1.0` state from `kv-creative-workbench`.

When working inside an IdeaCase, preserve IDs, constraints, evidence, and lineage. Follow `references/composition-contract.md`.

## Workflow

### 1. Read the original expression as a frame

Identify:

- key nouns and verbs;
- assumed actor;
- assumed goal;
- assumed medium or solution type;
- assumed user behavior;
- hidden evaluation rule;
- possibilities excluded by the wording.

Do not turn this into abstract philosophy. Every detected frame must affect a later question or candidate.

### 2. Loosen decisive terms

Select three to five terms. For each, record:

- default meaning;
- how it narrows the problem;
- alternative interpretations;
- what new solution space those alternatives open.

Use methods from `references/framing-methods.md`.

### 3. Create reframed questions

Generate five materially different questions. Change at least one of:

- actor;
- desired outcome;
- unit of value;
- time horizon;
- medium;
- behavior required from the user;
- scale;
- success criterion;
- opposite assumption.

A synonym swap is not a reframe.

### 4. Generate a diverse candidate set

Use `references/divergence-lenses.md`.

Generate five to eight candidates by default. Every candidate must include:

- stable ID;
- name;
- mechanism;
- target user or actor;
- use scenario;
- value created;
- novelty source;
- key assumption;
- frame that produced it.

Spread candidates across different mechanisms. Do not output five interfaces for the same underlying behavior.

### 5. Run the novelty test

Reject or repair candidates that are:

- ordinary ideas with unusual names;
- feature bundles without a causal mechanism;
- metaphors that cannot change design;
- dependent on an undefined super-intelligent AI;
- too similar to another candidate;
- disconnected from the user's constraints.

Keep imaginative candidates even when feasibility is uncertain, but label the uncertainty. Feasibility ranking belongs to convergence unless the user explicitly asks for it here.

### 6. Select exploration leads

Identify:

- strongest frame shift;
- most usable direction;
- most counterintuitive direction.

Do not declare a final winner. When composed with the workbench, pass the full clean candidate packet to convergence.

## Breakthrough discipline

Read `references/breakthrough-mode.md` before high-intensity work.

Use metaphors as design engines, not prose ornaments. A war metaphor must change actors, resources, timing, and failure conditions. A ritual metaphor must change repetition, commitment, symbolism, or social proof.

After a breakthrough pass, apply `references/de-dramatization.md`: retain mechanisms and remove inflated language, forced mysticism, and vague spectacle.

## Return signals

When working inside the suite:

- Return `EXPAND_DIVERSITY` only when a supplied frame set cannot produce mechanism-level variety without changing the root question.
- Return `REFRAME_ROOT` when the problem statement itself is misaligned with the user's goal.
- Return `REFRAME_TARGET_USER` when the mechanism is useful but the actor definition blocks value.
- Return a clean candidate packet when ready for blind convergence.

## Output behavior

Match the user's language. Keep explanations compact enough that candidates remain comparable.

For direct use, normally show:

1. Hidden frame.
2. Terms worth loosening.
3. Reframed questions.
4. Candidate set.
5. Three exploration leads.

When the user asks only for ideas, minimize process commentary and emphasize the candidates.

## References

- Suite handoff: `references/composition-contract.md`
- Reframing methods: `references/framing-methods.md`
- Candidate diversity: `references/divergence-lenses.md`
- Runtime modes: `references/modes.md`
- Breakthrough operation: `references/breakthrough-mode.md`
- Cleanup: `references/de-dramatization.md`
- Candidate format: `references/candidate-schema.md`
- Examples: `references/examples.md`
