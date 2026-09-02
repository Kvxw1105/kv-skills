# Browser adapter contract

The Skill does not depend on one browser implementation. Select the strongest available surface that satisfies the task.

## Minimum contract

An adapter should expose equivalent operations for:

1. connection and capability check;
2. list, open, claim, select, and identify tabs;
3. navigate and read the current URL;
4. targeted text/DOM/accessibility inspection;
5. click, type, keypress, select, and scroll;
6. wait for state changes or response completion;
7. screenshot when visual state matters;
8. upload and download handling when required;
9. explicit outcomes for writes: success, failure, or unknown;
10. protected confirmation for consequential submissions.

Do not treat “the browser panel is visible” as proof that the agent can control it.

## Surface selection

Prefer in order of task fit, not brand:

- A Harness-native browser when it can control the required signed-in session and supports the complete action set.
- A user-browser bridge when existing Chrome login state, extensions, file upload, or cross-Harness reuse matters.
- A generic Playwright/CDP browser for public pages, isolated testing, or repeatable QA where personal login state is unnecessary.
- Manual handoff only for unsupported trusted interactions or permission gates.

If the user explicitly names a browser surface, respect that choice.

## Cross-Harness bridge

For Harnesses without a capable native browser, a standard MCP browser bridge is the preferred portability layer. The controller Skill remains unchanged while only the tool mapping changes.

Map conceptual operations rather than hard-coding vendor tool names:

| Concept | Typical implementation |
|---|---|
| connection check | list tabs or status |
| targeted read | find/text/DOM snapshot |
| interaction | click/type/keypress |
| response wait | selector/state/text-change wait |
| artifact transfer | download status/path or file input assignment |
| write safety | explicit submit gate and unknown-outcome handling |

## Concurrency

When multiple agents share one browser, require a write lease per tab. Reads may be concurrent only if they cannot change focus or page state. Every operation should carry a client identity and target tab ID.

Do not retry an ambiguous write. Re-read page state first. Keep the result attributable to the worker that initiated it.

## Site adaptation

Chat interfaces change. Prefer semantic selectors and observable state over fixed coordinates. A site adapter should detect at least:

- signed-in versus signed-out;
- composer availability;
- generation active versus finished;
- latest assistant message boundary;
- context-limit or refusal state;
- downloadable artifact availability;
- authorization or confirmation gates.

Whole-page text alone is usually too stale and noisy for reliable generation-state detection.
