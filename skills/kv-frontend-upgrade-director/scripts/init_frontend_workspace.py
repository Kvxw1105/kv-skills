#!/usr/bin/env python3
"""Initialize persistent frontend-upgrade memory in a project."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from datetime import datetime, timezone


def write_if_missing(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return "kept"
    path.write_text(content, encoding="utf-8")
    return "written"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", required=True)
    p.add_argument("--project-name", required=True)
    p.add_argument("--project-type", default="unknown")
    p.add_argument("--force", action="store_true")
    args = p.parse_args()
    root = Path(args.project_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        p.error("--project-root must be an existing directory")
    agent = root / ".agent"
    agent.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat()
    outputs = {}
    context = (
        f'schema_version: 1\nproject: "{args.project_name}"\nproject_type: "{args.project_type}"\n'
        f'created_at: "{stamp}"\nmode: audit-upgrade\nprimary_user: ""\nprimary_job: ""\n'
        'core_routes: []\ncurrent_stack: []\nprotected_contracts: []\ndo_not_touch: []\n'
        'commands:\n  install: ""\n  dev: ""\n  lint: ""\n  typecheck: ""\n  build: ""\n  test: ""\n'
    )
    visual = (
        'schema_version: 1\nmain_archetype: ""\nsecondary_archetype: ""\nvisual_thesis: ""\n'
        'visual_authority: ""\nart_direction:\n  colors: []\n  typography: []\n  materials: []\n'
        '  motion_language: []\nshowcase_routes: []\nmobile_recomposition: []\n'
        'forbidden_patterns: []\nacceptance: []\n'
    )
    freeze = '# Functional Freeze\n\n## Must keep\n\n## Protected API / routes / auth / data\n\n## Allowed frontend changes\n\n## Explicitly forbidden\n\n## Rollback\n'
    handoff = '# Frontend Upgrade Handoff\n\n## Current state\n\n## Changed files\n\n## Tests and browser evidence\n\n## Unverified\n\n## Next highest-value action\n'
    outputs["frontend-upgrade-context.yaml"] = write_if_missing(agent/"frontend-upgrade-context.yaml", context, args.force)
    outputs["visual-baseline.yaml"] = write_if_missing(agent/"visual-baseline.yaml", visual, args.force)
    outputs["functional-freeze.md"] = write_if_missing(agent/"functional-freeze.md", freeze, args.force)
    outputs["findings.json"] = write_if_missing(agent/"findings.json", json.dumps({"schema_version":1,"findings":[]}, ensure_ascii=False, indent=2)+"\n", args.force)
    outputs["frontend-pattern-candidates.jsonl"] = write_if_missing(agent/"frontend-pattern-candidates.jsonl", "", args.force)
    outputs["handoff.md"] = write_if_missing(agent/"handoff.md", handoff, args.force)
    print(json.dumps({"project_root":str(root),"agent_dir":str(agent),"files":outputs}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
