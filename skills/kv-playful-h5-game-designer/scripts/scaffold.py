#!/usr/bin/env python3
"""Create a new single-file playful H5 prototype from the bundled starter."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a playful mobile H5 project")
    parser.add_argument("--out", required=True, help="Output project directory")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing index.html")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    starter = skill_root / "assets" / "starter" / "index.html"
    out_dir = Path(args.out).expanduser().resolve()
    target = out_dir / "index.html"

    if not starter.exists():
        raise FileNotFoundError(f"Starter file missing: {starter}")
    if target.exists() and not args.force:
        raise FileExistsError(f"Target already exists: {target}. Use --force to overwrite.")

    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(starter, target)
    (out_dir / "README.md").write_text(
        "# Playful H5 prototype\n\nOpen `index.html` in a browser. Edit the single file to iterate.\n",
        encoding="utf-8",
    )
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
