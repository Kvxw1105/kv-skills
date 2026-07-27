#!/usr/bin/env python3
"""Check that a preview HTML does not depend on local JS/CSS files or localhost."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LOCAL_SCRIPT_STYLE = re.compile(
    r'(?:src|href)=["\'](?!data:|https?:|//|#)[^"\']+\.(?:js|css)(?:\?[^"\']*)?["\']',
    re.IGNORECASE,
)
LOCALHOST = re.compile(r'https?://(?:localhost|127\.0\.0\.1)(?::\d+)?', re.IGNORECASE)
ABSOLUTE_PATH = re.compile(r'(?:[A-Za-z]:\\|/(?:home|Users|mnt|tmp)/)')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    args = parser.parse_args()

    if not args.html.is_file():
        print(f"ERROR: file not found: {args.html}", file=sys.stderr)
        return 1

    text = args.html.read_text(encoding="utf-8")
    problems: list[str] = []
    if LOCAL_SCRIPT_STYLE.search(text):
        problems.append("contains unresolved local JavaScript or CSS references")
    if LOCALHOST.search(text):
        problems.append("contains localhost URLs")
    if ABSOLUTE_PATH.search(text):
        problems.append("contains machine-specific absolute paths")
    if "<html" not in text.lower() or "</html>" not in text.lower():
        problems.append("does not look like a complete HTML document")
    if len(text.encode("utf-8")) < 256:
        problems.append("file is unexpectedly small")

    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1

    print(f"OK: standalone preview looks self-contained ({args.html.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
