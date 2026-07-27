#!/usr/bin/env python3
"""Compile modular frontend-upgrade prompts for coding agents."""
from __future__ import annotations
import argparse, re
from pathlib import Path

PROFILES = {
    "full": ["00"] + [f"{i:02d}" for i in range(1,21)] + ["90"],
    "existing-project": ["00","01","02","03","04","06","11","13","14","15","16","18","20","90"],
    "wow": ["00","02","05","06","07","08","09","10","11","13","14","15","17","18","90"],
    "workspace": ["00","03","04","06","11","13","14","16","18","19","20","90"],
    "h5": ["00","02","06","11","12","13","14","15","18","19","20","90"],
    "brand": ["00","02","04","05","06","07","08","09","10","13","14","15","17","18","20","90"],
    "patch": ["00","19","18","20","90"],
}


def parse_set(items: list[str]) -> dict[str,str]:
    result = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"invalid --set value: {item!r}; expected KEY=VALUE")
        k,v = item.split("=",1)
        result[k.strip()] = v
    return result


def find_module(directory: Path, module_id: str) -> Path:
    matches = sorted(directory.glob(f"{module_id}-*.md"))
    if not matches:
        raise FileNotFoundError(f"module {module_id} not found in {directory}")
    if len(matches) > 1:
        raise RuntimeError(f"module {module_id} is ambiguous: {matches}")
    return matches[0]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--profile", choices=sorted(PROFILES), default="existing-project")
    p.add_argument("--modules", help="comma-separated IDs; overrides profile")
    p.add_argument("--project", default="Untitled Project")
    p.add_argument("--set", action="append", default=[], metavar="KEY=VALUE")
    p.add_argument("--out")
    args = p.parse_args()
    directory = Path(__file__).resolve().parent.parent/"prompt-modules"
    ids = [x.strip().zfill(2) for x in args.modules.split(",")] if args.modules else PROFILES[args.profile]
    variables = {"PROJECT_NAME":args.project, **parse_set(args.set)}
    sections = [f"# {args.project} · KV Frontend Upgrade Prompt\n\nProfile: `{args.profile}`\nModules: `{', '.join(ids)}`\n"]
    for module_id in ids:
        text = find_module(directory,module_id).read_text(encoding="utf-8")
        for key,value in variables.items():
            text = text.replace("{{"+key+"}}", value)
        sections.append(text.strip())
    output = "\n\n---\n\n".join(sections)+"\n"
    if args.out:
        path = Path(args.out).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
        print(path.resolve())
    else:
        print(output, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
