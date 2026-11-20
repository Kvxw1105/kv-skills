#!/usr/bin/env python3
"""Validate structure and basic authorization consistency of a mission contract."""
import argparse
import json
from pathlib import Path

VALID_STATES = {
    "PROPOSED", "EVIDENCE_GATHERING", "OFFER_DRAFTED", "READY_TO_EXECUTE",
    "EXECUTED", "VERIFIED", "ARCHIVED", "BLOCKED_PERMISSION",
    "BLOCKED_CAPABILITY", "FAILED_TEST", "CANCELLED", "DISPUTED_EVIDENCE",
}


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["mission must be a JSON object"]
    for key in ("mission_id", "goal", "true_success", "mode", "authority", "tasks"):
        if key not in data:
            errors.append(f"missing {key}")
    auth = data.get("authority")
    if auth is not None and not isinstance(auth, dict):
        errors.append("authority must be an object")
        auth = {}
    if auth is None:
        auth = {}
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        return errors + ["tasks must be an array"]
    seen = set()
    for i, task in enumerate(tasks):
        if not isinstance(task, dict):
            errors.append(f"tasks[{i}] must be an object")
            continue
        for key in ("task_id", "owner_role", "goal", "status", "evidence_to_return"):
            if not task.get(key):
                errors.append(f"tasks[{i}] missing or empty {key}")
        task_id = task.get("task_id")
        if task_id in seen:
            errors.append(f"duplicate task_id {task_id}")
        seen.add(task_id)
        state = task.get("status")
        if state not in VALID_STATES:
            errors.append(f"invalid task status {state}")
        if task.get("requires_external_action") and not (auth.get("outreach") or auth.get("publish") or auth.get("payment")):
            errors.append(f"task {task_id} requires external action without any applicable authorization")
    if data.get("state") and data["state"] not in VALID_STATES:
        errors.append("invalid mission state")
    if data.get("spending_limit", 0) is None or data.get("spending_limit", 0) < 0:
        errors.append("spending_limit must be >= 0")
    if auth.get("payment") and not data.get("spending_limit", 0):
        errors.append("payment enabled but spending_limit is missing/zero")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mission_json", type=Path)
    args = parser.parse_args()
    errors = validate(json.loads(args.mission_json.read_text(encoding="utf-8")))
    if errors:
        print("INVALID\n" + "\n".join("- " + msg for msg in errors))
        raise SystemExit(1)
    print("VALID mission contract (structural checks only; not a permission grant)")


if __name__ == "__main__":
    main()
