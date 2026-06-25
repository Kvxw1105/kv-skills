# Design Notes

This file preserves the thinking behind Blind Spot Mirror. Runtime instructions live in `../SKILL.md`; this document explains why the runtime is shaped that way.

## Core thesis

Blind Spot Mirror treats the AI agent as a professional with blind spots, not as a child that needs punishment. The goal is awareness, not compliance theater.

The mirror should help the agent notice the moments when its own fluency, helpfulness, confidence, or tool access becomes dangerous:

- fluency can hide fake completion
- helpfulness can create scope drift
- confidence can outlive the freshness of knowledge
- tool access can be forgotten at the exact moment it matters
- agreement can become sycophancy

## Why v2 is shorter

The original version was strong as an essay and taxonomy, but heavy as a runtime skill. v2 separates the two jobs:

- `SKILL.md` is the low-friction runtime layer.
- `references/` keeps the deeper theory, chains, domains, anti-patterns, and tests.

A runtime skill must create better outputs, not better self-description. If the agent spends too much time talking about its metacognition, the skill has failed.

## Why not "always use"

The mirror is broadly applicable, but not every task deserves the same self-check cost. A trivial one-step answer should not pay the same cognitive tax as a multi-file code change or high-stakes research claim.

v2 uses depth selection:

- skip or silent glance for trivial work
- light check for simple factual work
- standard check for multi-step work
- full check for high-risk or ambiguous work

This prevents the skill from becoming checkbox theater.

## Why triage comes before taxonomy

Seven failure modes are useful for understanding failures, but too much taxonomy slows runtime decisions. v2 asks four operational questions first:

1. Am I claiming specifics I have not verified?
2. Am I explaining instead of doing?
3. Am I still solving the original request?
4. Is my language carrying mood instead of information?

These questions route to the failure modes without forcing the agent to classify perfectly.

## What must remain quiet

The mirror is internal. The user should usually not see labels like Fake Completion or Scope Drift. They should see:

- more verified facts
- fewer unsupported claims
- more direct execution
- tighter scope
- clearer pushback when needed

Public self-awareness is only useful when the user asks for a critique or audit trail.

## Product direction

The next maturity step is evaluation, not more theory. The existing `references/tests/` scenarios should become a repeatable eval set comparing:

- original skill
- v2 runtime skill
- no skill baseline

The key question is not whether the framework sounds right, but whether it improves outputs without adding excessive time or token cost.
