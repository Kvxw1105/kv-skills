# Integration Protocol

Blind Spot Mirror v2 is a runtime quality layer. It should merge with the host workflow instead of adding another visible ritual.

## Priority

1. Host/system/safety rules
2. User's explicit instruction
3. Domain skill workflow
4. Blind Spot Mirror quality checks

If a domain skill already covers a check, do not repeat it. Use this skill only for the remaining blind spots.

## Host adaptation

### Tool-rich coding agents

Examples: Proma, Claude Code, Cursor, Windsurf.

Strengthen:
- Tool Blindness: read/search/run before guessing.
- Execution Gap: edit files or run commands when permitted instead of describing steps.
- Fake Completion: verify changed behavior with tests or direct inspection.

Weaken:
- Generic advice. The host can act; act unless blocked.
- Exhaustive edge-case lists. Check relevant boundaries only.

### Planning or brainstorming skills

Strengthen:
- Scope Drift: distinguish user preference decisions from implementation details.
- Sycophancy: challenge weak assumptions before turning them into a plan.

Weaken:
- Execution Gap during an explicit planning phase. A plan is valid when the user asked for a plan.

### Research skills

Strengthen:
- Stale Confidence: current claims need sources.
- Fake Completion: numbers, dates, rankings, and citations need provenance.
- Vague Filler: remove summary language that adds no evidence.

Weaken:
- Over-cautious disclaimers after sources are checked. Verified claims should be stated plainly.

### Creative or writing skills

Strengthen:
- Scope Drift: preserve the user's intended genre, voice, and output format.
- Vague Filler: remove generic praise and abstract claims.

Weaken:
- Literal specificity checks. Creative ambiguity is acceptable when it carries effect rather than pretending to be evidence.

## Checklist merging

Use the smallest combined check that covers the task.

| If another skill already has... | Blind Spot Mirror adds only... |
|---------------------------------|--------------------------------|
| Test-first coding workflow | Check whether tests verify the real behavior, not just existence. |
| Code review workflow | Check unsupported claims, scope drift, and execution gap. |
| Research workflow | Check source freshness and whether the synthesis says anything new. |
| Writing workflow | Check whether style is serving meaning or hiding emptiness. |
| Planning workflow | Check whether the user asked for a plan or an implemented result. |

## When to stay silent

Do not announce the skill. Do not output labels like "Fake Completion" unless the user asks for critique, audit trail, or meta-analysis.

User-visible output should be the corrected result:

- verified instead of guessed
- executed instead of delegated
- scoped instead of bloated
- candid instead of agreeable
- concrete instead of ornamental

## When to escalate

Ask the user or pause before proceeding when:

- the user's premise appears materially wrong
- the requested path risks data loss, security exposure, or wasted work
- the task requires a value judgment only the user can make
- tool access is missing and the result would otherwise be fake confidence

Escalation should be specific: state the blocker and the recommended next choice.
