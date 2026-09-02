---
name: kp-chatgpt-web-orchestrator
description: "[kp-] Orchestrate a signed-in ChatGPT Web session as a supervised second execution engine from any capable Agent Harness. Use when browser-accessible ChatGPT memory, personalization, Skills, connectors, deep research, multimodal work, or artifact generation can materially improve a task. Routes work between the controlling agent and ChatGPT Web, supervises continuation, verifies results, and persists useful artifacts. Requires a browser-control adapter; do not use merely for generic web lookup or to bypass platform limits."
metadata:
  version: 1.0.0
  ip-prefix: kp
  author: "心吾"
  visibility: public
  role: product
  publish_target: kv-skills
  memory_policy: public
---

# ChatGPT Web Orchestrator

Use ChatGPT Web as a supervised worker, not as an unsupervised replacement for the controlling agent.

The controlling agent owns the user's final objective, task routing, durable state, local execution, verification, and delivery. ChatGPT Web contributes account-specific memory, personalization, Skills, connectors, research, synthesis, multimodal generation, and artifact tools.

Optimize for result quality per unit of coordination. Do not minimize controller usage at the cost of reliability.

## Requirements

This Skill is Harness-agnostic, but execution requires equivalent capabilities:

- open or claim a browser tab with a signed-in ChatGPT Web session;
- inspect visible page state and the latest assistant response;
- click, type, submit, scroll, wait, and preferably download artifacts;
- read and write durable files outside the chat;
- retain controller state across multiple Web rounds.

Read [references/browser-adapters.md](references/browser-adapters.md) when choosing or configuring the browser surface.

## Authorization boundary

Conversation-level actions may proceed only when the user or current Harness policy authorizes them. Do not infer a standing permission from this public Skill.

Always preserve confirmation gates for deleting or archiving chats, changing account settings, OAuth or connector authorization, purchasing, publishing, messaging third parties, production mutations, or other consequential external actions.

Use visible signed-in UI. Never inspect or export passwords, cookies, browser storage, profiles, tokens, or session databases. Do not use this workflow to evade rate limits, account restrictions, billing, or platform safeguards.

## Route the work

Delegate to ChatGPT Web when it offers a material advantage:

- account memory, custom instructions, or personal voice should affect the result;
- a Web Skill or connected app can perform substantive work;
- deep research, multi-source synthesis, multimodal generation, or office-file creation compresses many operations into one deliverable;
- an independent model perspective improves architecture, critique, red-teaming, or acceptance judgment;
- the work package can run in parallel while the controller performs local work.

Keep work in the controlling agent when it is mainly repository editing, shell execution, tests, builds, precise filesystem work, short factual work, or when sending and reading the delegation costs more than direct execution.

For substantial tasks, use this loop:

`Controller frames and routes -> ChatGPT Web executes or critiques -> Controller verifies and integrates -> targeted continuation if needed`

Do not duplicate the entire reasoning process on both sides.

## Efficient supervision

Waiting does not require continuous model reasoning. Poll at sensible intervals and perform independent work while Web runs when possible.

- Request a compact executive result plus a complete artifact, not narrated hidden reasoning.
- Require evidence, decisions, risks, and next actions in stable sections.
- Prefer native files when formatting or download is part of the outcome.
- Prefer a single Markdown block when content will be indexed, diffed, transformed, or merged locally.
- Read the newest response or changed section instead of repeatedly ingesting the full chat.
- Request deltas on later rounds: corrections, missing evidence, or replacement sections.
- Use multiple tabs only for genuinely independent work packages and keep outputs attributable.

Delegation is efficient when Web performs many internal operations and returns a compact, high-value result. It is inefficient when the controller transmits huge context, reads a huge response, and repeats the same work.

## Operating loop

1. Define the observable final outcome, constraints, acceptance checks, and protected boundaries.
2. Split work between the controller, ChatGPT Web, or parallel independent workers.
3. Select and verify a browser adapter. Reuse a suitable signed-in session; do not assume a displayed page is controllable.
4. Choose a normal persistent chat for durable, personalized, Skill-heavy work. Use a temporary chat only for disposable exploration after confirming whether it provides the required personalization and tools.
5. Send a self-contained work order using [references/prompt-protocols.md](references/prompt-protocols.md). Name the most specific relevant Web Skill when known; never request every Skill by default.
6. Wait without busy-looping. Observe generation state and stop conditions from the current page rather than stale whole-page text.
7. Read the newest deliverable and validate claims against files, sources, code, runtime behavior, or acceptance criteria.
8. Accept and integrate, send a precise correction, change strategy after repeated failure, or pause for a genuine permission/data gate.
9. Persist valuable outputs with provenance and verification status.
10. Deliver the actual result. Delegation, waiting, a plan, or a polished Web response is not completion.

## Long-horizon controller state

ChatGPT Web does not own the long-running goal. Maintain durable controller state:

- final objective and acceptance criteria;
- completed and verified outputs;
- key decisions and evidence;
- current blockers and permission gates;
- exact next work package.

Request a compact `[STATE]` block at checkpoints. Resume with that state plus only changed context. Send a bare “continue” only when the prior next action is unambiguous; otherwise target the actual acceptance gap.

If the chat reaches its context limit, persist state and continue in a fresh chat. Do not repeatedly send into a saturated thread.

## Quality gates

Treat Web output as a candidate until verified:

- claiming a Skill was used is not proof it was loaded or executed;
- claiming a file was generated is not proof until it exists and opens;
- claiming code works is not proof until relevant tests or runtime checks pass;
- dynamic facts need current sources;
- connector availability is not proof of current authorization;
- a polished response is not proof that the user's outcome is met.

After two materially similar failed attempts, inspect the cause and change the prompt, chat, mode, tool, browser surface, or division of labor instead of repeating blindly.

## Example invocations

```text
$kp-chatgpt-web-orchestrator Use my signed-in ChatGPT Web to research the current ecosystem and create the report. You remain responsible for source checks and saving the verified report locally.
```

```text
$kp-chatgpt-web-orchestrator Ask ChatGPT Web to independently review this architecture while you continue the local implementation. Reconcile both results against the acceptance criteria.
```

## Common failure modes

- **Using Web for every task:** route short or local work directly to the controller.
- **Sending only “continue”:** identify the unmet acceptance criterion and send a targeted correction.
- **Reading the full page repeatedly:** read the latest response boundary or changed artifact.
- **Confusing a visible panel with an adapter:** prove control with a read-only connection call first.
- **Retrying an ambiguous submit:** inspect current page state before any retry.
- **Trusting self-reported completion:** verify files, sources, code, and runtime behavior outside the chat.
