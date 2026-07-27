#!/usr/bin/env python3
"""Create a new H5 prototype from the bundled adaptive starter."""
from __future__ import annotations
import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a lightweight H5 game project")
    parser.add_argument("--out", required=True, help="Output directory")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing index.html")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    starter = skill_root / "assets" / "starter" / "index.html"
    out_dir = Path(args.out).expanduser().resolve()
    target = out_dir / "index.html"

    if not starter.exists():
        raise FileNotFoundError(f"Starter not found: {starter}")
    if target.exists() and not args.force:
        parser.error(f"{target} already exists; pass --force to overwrite")

    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(starter, target)
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
