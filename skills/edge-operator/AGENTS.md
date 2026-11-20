# Instructions for AI coding and research agents

This directory is the portable source of truth for Edge Operator v1.0.

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
1. Run `python scripts/test_contracts.py -v`.
2. Run `python scripts/validate_mission.py templates/mission.json`.
3. Verify `python scripts/package.py --out ./dist/skill.zip` creates one skill folder.
4. Scan changed files for secrets, private data, copied text and unlicensed assets.
5. Update `CHANGELOG.md`, link to measured behavior where possible.
