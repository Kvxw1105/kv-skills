---
name: kv-goal-loop-chatgpt
description: Run a bounded, same-turn plan-execute-verify-evaluate loop for complex goals in ChatGPT. Use when the user asks for goal mode, 自主循环、自动迭代、做到完成为止、持续优化、loop engineering, or gives a high-level multi-step objective that benefits from repeated execution and tool-based verification. The loop must complete within the current response/tool session, normally in no more than three rounds, and must never promise background or unattended continuation. Do not trigger for simple one-step tasks, pure questions, or work whose success cannot be meaningfully checked.
---

# KV Goal Loop for ChatGPT

Turn a high-level objective into a bounded execution loop inside the current response. Progress comes from evidence-producing feedback, not from repeating plans.

## Non-negotiable runtime boundary

- Work only in the current response and available tool session.
- Never promise to continue after replying, run unattended, or deliver later.
- Default to a maximum of **three rounds**. Use fewer when the goal is achieved earlier.
- A round must produce a material action or new verification evidence. Pure rewording does not count.
- When a future scheduled action is genuinely requested, use the automation tool instead of this loop.

## Phase 0: Define the contract

Extract or infer:

- **Objective**: the actual result the user needs.
- **Success criteria**: observable or machine-checkable conditions.
- **Constraints**: tools, time, scope, format, safety, compatibility.
- **Evidence sources**: tests, builds, screenshots, file inspection, citations, diff, calculations, or explicit user criteria.

When information is incomplete but progress is possible, state a narrow assumption and proceed. Ask only when the missing fact blocks meaningful execution.

## Round structure

### 1. Plan

Choose the smallest set of actions likely to change the result. Prioritize by dependency, impact, and information value. Avoid planning the entire universe.

### 2. Execute

Perform the work with available tools. Group independent reads or checks when useful. Keep the user informed during long work according to the conversation’s update rules.

### 3. Verify

Use the strongest available evidence in this order when relevant:

1. automated tests or deterministic checks,
2. build/type/lint validation,
3. opening or rendering the produced artifact,
4. structured source comparison or diff,
5. direct inspection of the critical path,
6. reasoned evaluation clearly labeled as judgment.

Never substitute “looks correct” for a check that can actually be run.

### 4. Evaluate

Compare evidence against each success criterion:

- **Pass**
- **Partial**
- **Fail**
- **Unverifiable in this environment**

Identify the single highest-leverage gap. Do not generate a broad new backlog unless the user requested one.

### 5. Decide

- All criteria pass: stop and deliver.
- A concrete fix remains and another round can materially improve the result: continue.
- The same failure repeats twice: change method, tool, or framing.
- A required permission, file, credential, or capability is unavailable: stop with the exact blocker and best completed output.
- The round budget is exhausted: deliver the best verified state and a precise continuation point.

## Stagnation rules

Treat these as stagnation signals:

- two rounds produce essentially the same error,
- verification provides no new evidence,
- changes are cosmetic while the core criterion still fails,
- the proposed next action depends on an unavailable capability.

On stagnation, switch method once. Do not keep looping to simulate persistence.

## Working state

For file-based or coding tasks, maintain a concise state file when useful:

```markdown
# Goal State
Objective:
Success criteria:
Constraints:
Round:
Completed evidence:
Open gap:
Next action:
```

Do not create state files for ordinary conversational tasks where they add clutter.

## Final delivery

State:

1. what was completed,
2. verification evidence,
3. which success criteria passed or remain partial,
4. files or artifacts produced,
5. the exact blocker or continuation point when incomplete.

Do not hide partial completion behind a confident summary.
