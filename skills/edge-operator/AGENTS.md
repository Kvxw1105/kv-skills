# Instructions for AI coding and research agents

This directory is the portable source of truth for Edge Operator v1.1.

## Before edits
- Read `SKILL.md`, `README.md`, and only the reference material relevant to the requested change.
- Decide whether the task is focused patch, behavior redesign, new atom, new role, or protocol change.
- Preserve user-locked goals; keep speculative opportunities separate from validated market evidence.
- Check for license or personal/private data before adding externally sourced content.

## Editing rules
- Keep `SKILL.md` as a focused control plane, detailed knowledge in `references/` and host-specific instructions in `prompts/`.
- New thinking atoms must specify an observation, a question, a usable action, a falsifier, and a condition where it should **not** be applied.
- Distinguish **analysis of abuse** from **operational abuse**. Do not create covert data collection, credential abuse, fraudulent claims or harassment workflows.
- Do not hard-code owner identities, local paths, environment-specific tool availability or third-party API credentials.
- Preserve `templates/mission.json` and `templates/permission_charter.yaml` as publicly safe examples rather than real permissions.
- Run Python standard-library tests and mission validation after changes; record limitations and failures.

## Cross-agent contracts
- Keep task IDs, deliverable paths, status, evidence types and acceptance criteria explicit.
- Never upgrade `PROPOSED` or `PREPARED` to completed without the actual receipt or test output.
- Keep real-world actions inside currently valid, explicit authorization and available tools.

## Release checklist
1. Run `python -m unittest discover -s scripts -p "test_*.py" -v` and `python scripts/evidence_gate.py examples/etsy-authenticity-2026/opportunity-evidence.json --json`.
2. Run `python scripts/validate_mission.py templates/mission.json`.
3. Verify `python scripts/package.py --out ./dist/skill.zip` creates one skill folder.
4. Scan changed files for secrets, private data, copied text and unlicensed assets.
5. Update `CHANGELOG.md`, link to measured behavior where possible.

- For sourced new thinking atoms, link `research-atoms.json` to `research-source-ledger.json`, add realistic counterexamples to `test_research.py`, never infer payments from offer listings.


## v1.2 forecast integrity and atom retirement

- Original 96 heuristic atoms must remain `heuristic` until a documented test changes evidence level; source-linked RX atoms are not field validated by citation alone. Registry `references/atom-registry.json` is the portable sidecar. Do not regenerate it destructively after lifecycle edits.
- On actionable opportunities: complete an outside-view direction card, competing disconfirming hypotheses, value-bottleneck/decay map and a frozen forecast with numeric p/falsifier/settlement date. Unknown base rates remain unknown.
- Do not edit forecast probabilities, cohort or settlement deadlines after freezing. Revise via a new forecast ID; preserve old SHA and evidence receipts. VOID unattainable tests rather than recording demand failure.
- Compare atoms only on blinded/controlled eligible tasks, with explicit context and results; one commercial win does not validate all concurrently invoked atoms. Retired atoms stay archived and should not be chosen by default.
- Make user-facing orientation and settlement packets; never claim the user was informed, a monthly automation installed or a payment received without a trace.
- Run all `test_*.py` and validate/score the bundled zero-real-data examples before releasing. All examples must be overtly hypothetical.
