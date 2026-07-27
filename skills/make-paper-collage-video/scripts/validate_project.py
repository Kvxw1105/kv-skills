#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ALLOWED_PATTERNS = {"free", "supported-subject", "registered-environment"}
ALLOWED_KINDS = {"asset", "group"}


def err(errors: list[str], message: str) -> None:
    errors.append(message)


def check_keyframes(errors: list[str], motion: dict[str, Any], path: str) -> None:
    keyframes = motion.get("keyframes", [])
    if not isinstance(keyframes, list) or len(keyframes) < 2:
        err(errors, f"{path}.motion.keyframes must contain at least two entries")
        return
    ats = []
    for i, frame in enumerate(keyframes):
        if not isinstance(frame, dict) or "at" not in frame:
            err(errors, f"{path}.motion.keyframes[{i}] must be an object with at")
            continue
        at = frame["at"]
        if not isinstance(at, (int, float)) or not 0 <= at <= 1:
            err(errors, f"{path}.motion.keyframes[{i}].at must be within 0..1")
        ats.append(at)
    if ats and ats != sorted(ats):
        err(errors, f"{path}.motion.keyframes must be sorted by at")
    if ats and ats[0] != 0:
        err(errors, f"{path}.motion.keyframes must start at 0")
    if ats and ats[-1] != 1:
        err(errors, f"{path}.motion.keyframes must end at 1")


def walk_node(errors: list[str], node: Any, path: str, ids: set[str]) -> None:
    if not isinstance(node, dict):
        err(errors, f"{path} must be an object")
        return
    node_id = node.get("id")
    if not isinstance(node_id, str) or not node_id:
        err(errors, f"{path}.id is required")
    elif node_id in ids:
        err(errors, f"duplicate node id: {node_id}")
    else:
        ids.add(node_id)
    kind = node.get("kind")
    if kind not in ALLOWED_KINDS:
        err(errors, f"{path}.kind must be asset or group")
        return
    transform = node.get("transform")
    if not isinstance(transform, dict):
        err(errors, f"{path}.transform is required")
    check_keyframes(errors, node.get("motion", {}), path)
    if kind == "group":
        pattern = node.get("pattern")
        if pattern not in ALLOWED_PATTERNS:
            err(errors, f"{path}.pattern is invalid")
        children = node.get("children", [])
        if not isinstance(children, list) or not children:
            err(errors, f"{path}.children must be a non-empty list")
        else:
            for i, child in enumerate(children):
                walk_node(errors, child, f"{path}.children[{i}]", ids)
        if pattern in {"supported-subject", "registered-environment"} and not node.get("registration"):
            err(errors, f"{path}.registration is required for {pattern}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a portable paper-collage project")
    parser.add_argument("project")
    args = parser.parse_args()
    path = Path(args.project).resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    if data.get("schemaVersion") != 4:
        err(errors, "schemaVersion must be 4")
    video = data.get("video", {})
    for key in ("width", "height", "fps"):
        if not isinstance(video.get(key), int) or video[key] <= 0:
            err(errors, f"video.{key} must be a positive integer")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        err(errors, "scenes must be a non-empty list")
    else:
        scene_ids: set[str] = set()
        for si, scene in enumerate(scenes):
            sp = f"scenes[{si}]"
            sid = scene.get("id") if isinstance(scene, dict) else None
            if not isinstance(sid, str) or not sid:
                err(errors, f"{sp}.id is required")
                continue
            if sid in scene_ids:
                err(errors, f"duplicate scene id: {sid}")
            scene_ids.add(sid)
            proofs = scene.get("proofTimes", [])
            if not isinstance(proofs, list) or len(proofs) < 3:
                err(errors, f"{sp}.proofTimes must contain establish, action/peak, and final")
            else:
                final = [p for p in proofs if isinstance(p, dict) and p.get("kind") == "final"]
                if not final or max(float(p.get("at", 0)) for p in final) < 0.82:
                    err(errors, f"{sp} must have a final proof at or after 0.82")
            nodes = scene.get("composition", {}).get("nodes", [])
            ids: set[str] = set()
            if not isinstance(nodes, list) or not nodes:
                err(errors, f"{sp}.composition.nodes must be non-empty")
            else:
                for ni, node in enumerate(nodes):
                    walk_node(errors, node, f"{sp}.composition.nodes[{ni}]", ids)
            cues = scene.get("cues", [])
            if not isinstance(cues, list):
                err(errors, f"{sp}.cues must be a list")
            for ci, cue in enumerate(cues if isinstance(cues, list) else []):
                target = cue.get("targetId") if isinstance(cue, dict) else None
                if target not in ids and target != sid:
                    err(errors, f"{sp}.cues[{ci}].targetId does not exist: {target}")

    result = {"valid": not errors, "errors": errors, "warnings": warnings, "project": str(path)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
