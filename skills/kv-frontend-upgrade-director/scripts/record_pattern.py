#!/usr/bin/env python3
"""Append a structured frontend pattern candidate to project memory."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from datetime import datetime, timezone


def slugify(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", text.strip()).strip("-").lower()
    return value[:60] or "pattern"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--problem", required=True)
    p.add_argument("--solution", required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--transfer", required=True)
    p.add_argument("--cost", default="")
    p.add_argument("--boundary", default="")
    p.add_argument("--status", choices=["candidate","validated","promoted"], default="candidate")
    args = p.parse_args()
    root = Path(args.project_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        p.error("--project-root must be an existing directory")
    agent = root/".agent"
    agent.mkdir(exist_ok=True)
    out = agent/"frontend-pattern-candidates.jsonl"
    record = {
        "schema_version": 1,
        "id": f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{slugify(args.title)}",
        "title": args.title,
        "problem": args.problem,
        "solution": args.solution,
        "evidence": args.evidence,
        "transfer": args.transfer,
        "cost": args.cost,
        "boundary": args.boundary,
        "status": args.status,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False)+"\n")
    print(json.dumps({"written":str(out),"record":record}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
