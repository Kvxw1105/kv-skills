#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Read portable production state")
    parser.add_argument("production")
    args = parser.parse_args()
    path = Path(args.production).resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    control = data.get("control", {})
    remaining = control.get("workItems", {}).get("remaining", [])
    result = {
        "slug": data.get("slug"),
        "stage": data.get("stage"),
        "mode": control.get("mode"),
        "nextCommand": control.get("nextCommand"),
        "nextWorkItem": remaining[0] if remaining else None,
        "complete": data.get("stage") == "complete",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
