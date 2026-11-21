# Host adapters: official conventions and limits

Checked against vendor documentation in **2026-11-21**; tested with actual filesystem sandboxes, **not** logged-in GUI instances of every host. Provider policies, versions and project settings may differ.

| Agent | Official documentation | Project-scoped adapter |
|---|---|---|
| Codex | https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide ; https://developers.openai.com/api/reference/cli | AGENTS.md + .agents/skills/ |
| Claude Code | https://docs.anthropic.com/en/docs/claude-code/memory | CLAUDE.md + .claude/skills/ |
| Gemini CLI | https://geminicli.com/docs/cli/gemini-md/ ; https://geminicli.com/docs/cli/skills/ | GEMINI.md + .gemini/skills/ |
| OpenCode | https://opencode.ai/docs/instructions ; https://opencode.ai/docs/skills | AGENTS.md + .opencode/skills/ |
| Cursor | https://docs.cursor.com/context/rules-for-ai | .cursor/rules/edge-operator.mdc (alwaysApply: false) |
| OpenClaw | https://docs.openclaw.ai/concepts/agent-workspace | workspace AGENTS.md (operations) + SOUL.md (tone) + skills/ |

**SOUL.md is not universal**: it has specific meaning in OpenClaw and is not generally an AGENTS.md replacement. This adapter appends only business-task tone guidance without rewriting identity or personal preferences.

**System prompt is runtime-controlled**. A project file or exported prompt cannot supersede vendor system-level rules or grant network, accounts, funds or tool permissions. `export` makes a plain text prompt to paste into the *supported* external UI field.

**Mika, NanoMuse, Muse, Grokbot, ChatGPT**: their project config paths and editing APIs are not established here. Use prompt-only export and verify supported UI fields; do not claim any automatic installation or background sync.

**Install verification**: run `status` then start a fresh host session; check actual skill discovery and ask about copied promotional posts, checking three hypotheses rather than instantly accusing shills. Also test an unrelated creative request for accidental commercial prompt bleed. `status` only verifies local files, not that a provider honored their contents.

**Multiple hosts**: one project can contain several managed snippets. That may cost context on hosts reading AGENTS.md twice; install only the needed targets or compare and remove duplicate adapters.
