#!/usr/bin/env python3
"""Record an approved learning candidate for the interactive IP profit skill.

Default behavior appends a structured entry to references/evolution-inbox.md.
Use --promote only after manual review to also append a concise rule to a target
reference file and add an entry to references/evolution-log.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ALLOWED_CATEGORIES = {
    "creative",
    "ip",
    "monetization",
    "production",
    "platform",
    "safety",
    "workflow",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}


def clean(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    return value


def require_text(name: str, value: str) -> str:
    value = clean(value)
    if not value:
        raise ValueError(f"{name} must not be empty")
    return value


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Record a user-approved learning candidate in the skill source."
    )
    parser.add_argument("--skill-dir", required=True, help="Path to the skill source directory")
    parser.add_argument("--title", required=True)
    parser.add_argument("--category", required=True, choices=sorted(ALLOWED_CATEGORIES))
    parser.add_argument("--summary", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--target-file", required=True, help="Relative path inside the skill directory")
    parser.add_argument("--target-section", default="待归类")
    parser.add_argument("--confidence", default="medium", choices=sorted(ALLOWED_CONFIDENCE))
    parser.add_argument("--time-sensitive", action="store_true")
    parser.add_argument("--supersedes", default="")
    parser.add_argument(
        "--promote",
        action="store_true",
        help="After review, append the rule to the target reference and evolution log",
    )
    args = parser.parse_args()

    try:
        skill_dir = Path(args.skill_dir).expanduser().resolve()
        if not skill_dir.is_dir():
            raise ValueError(f"skill directory does not exist: {skill_dir}")
        if not (skill_dir / "SKILL.md").exists():
            raise ValueError("SKILL.md not found in skill directory")

        title = require_text("title", args.title)
        summary = require_text("summary", args.summary)
        evidence = require_text("evidence", args.evidence)
        target_section = require_text("target-section", args.target_section)
        supersedes = clean(args.supersedes)

        target_rel = Path(args.target_file)
        if target_rel.is_absolute() or ".." in target_rel.parts:
            raise ValueError("target-file must be a safe relative path")
        if target_rel.suffix.lower() != ".md":
            raise ValueError("target-file must be a markdown file")

        today = dt.date.today().isoformat()
        inbox = skill_dir / "references" / "evolution-inbox.md"
        entry = (
            f"\n## {today} · {title}\n\n"
            f"- category: `{args.category}`\n"
            f"- summary: {summary}\n"
            f"- evidence: {evidence}\n"
            f"- target: `{target_rel.as_posix()}` → {target_section}\n"
            f"- confidence: `{args.confidence}`\n"
            f"- time_sensitive: `{str(args.time_sensitive).lower()}`\n"
            f"- supersedes: {supersedes or '无'}\n"
            f"- approved_by_user: `true`\n"
            f"- status: `{'promoted' if args.promote else 'inbox'}`\n"
        )
        append_text(inbox, entry)

        if args.promote:
            target = (skill_dir / target_rel).resolve()
            if skill_dir not in target.parents:
                raise ValueError("target-file resolves outside the skill directory")
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"# {target.stem.replace('-', ' ').title()}\n", encoding="utf-8")
            promoted = (
                f"\n### {title}\n\n"
                f"{summary}\n\n"
                f"来源与证据：{evidence}。可信度：{args.confidence}。"
                f"{'此规则具有时效性。' if args.time_sensitive else ''}\n"
            )
            append_text(target, promoted)

            log = skill_dir / "references" / "evolution-log.md"
            log_entry = (
                f"\n## {today}\n\n"
                f"- 晋升经验“{title}”到 `{target_rel.as_posix()}` 的“{target_section}”；"
                f"分类 `{args.category}`，可信度 `{args.confidence}`。\n"
            )
            append_text(log, log_entry)

        print(f"recorded: {title}")
        print(f"inbox: {inbox}")
        if args.promote:
            print(f"promoted_to: {skill_dir / target_rel}")
        return 0
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
