#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    if not value:
        raise ValueError("slug must contain at least one ASCII letter or digit")
    return value


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a portable paper-collage workspace")
    parser.add_argument("--target", required=True, help="Writable workspace directory")
    parser.add_argument("--slug", required=True, help="Lowercase project slug")
    parser.add_argument("--title", required=True, help="Human-readable project title")
    parser.add_argument("--force", action="store_true", help="Allow writing into an existing empty project directory")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    slug = slugify(args.slug)
    project_dir = target / "projects" / slug
    if project_dir.exists() and any(project_dir.iterdir()) and not args.force:
        raise SystemExit(f"project already exists and is not empty: {project_dir}")

    template = Path(__file__).resolve().parents[1] / "assets" / "runtime-template"
    target.mkdir(parents=True, exist_ok=True)
    for item in template.iterdir():
        destination = target / item.name
        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
        elif not destination.exists() or args.force:
            shutil.copy2(item, destination)

    now = datetime.now(timezone.utc).isoformat()
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "requests").mkdir(exist_ok=True)
    (project_dir / "assets").mkdir(exist_ok=True)

    brief = f"""# {args.title}\n\n## Purpose\nDescribe the audience, outcome, facts, style, rights, prohibitions, and delivery format.\n\n## Medium decision\nChoose one: layered collage / articulated code cut-paper.\n"""
    (project_dir / "brief.md").write_text(brief, encoding="utf-8")

    production = {
        "schemaVersion": 1,
        "slug": slug,
        "stage": "capability-review",
        "control": {
            "mode": "human-gate",
            "nextCommand": "prepare-concept-decision",
            "workItems": {"remaining": ["concept", "storyboard", "provider-plan"]},
        },
        "approvals": [],
        "artifacts": [],
        "events": [{"at": now, "type": "project-created", "note": "portable workspace"}],
    }
    write_json(project_dir / "production.json", production)

    storyboard = {
        "schemaVersion": 1,
        "slug": slug,
        "arc": "establish → action → consequence",
        "sharedVisualLanguage": "layered paper collage with visible depth and restrained motion",
        "scenes": [
            {
                "id": "scene-01",
                "label": "Opening tableau",
                "blueprint": "layered-reveal",
                "estimatedDurationSeconds": 6,
                "beats": [
                    {"id": "establish", "at": 0.12, "action": "establish the space"},
                    {"id": "action", "at": 0.52, "action": "trigger the central event"},
                    {"id": "final", "at": 0.86, "action": "preserve the consequence"},
                ],
                "compositionPlan": {"patterns": ["free"], "relationships": []},
                "proofTimes": [
                    {"id": "establish", "at": 0.12, "kind": "establish", "assertions": ["space and primary subject are readable"]},
                    {"id": "action", "at": 0.52, "kind": "action", "assertions": ["the central event is visibly occurring"]},
                    {"id": "final", "at": 0.86, "kind": "final", "assertions": ["the consequence remains visible"]},
                ],
            }
        ],
    }
    write_json(project_dir / "storyboard.json", storyboard)

    project = {
        "schemaVersion": 4,
        "slug": slug,
        "title": args.title,
        "video": {"width": 1280, "height": 720, "fps": 30},
        "theme": {
            "canvas": "#0d0b0a",
            "paper": "#d8c7a7",
            "ink": "#17110d",
            "accent": "#d56b37",
            "paperEdge": "#f1dfbd",
        },
        "scenes": [
            {
                "id": "scene-01",
                "label": "Opening tableau",
                "durationSeconds": 6,
                "camera": {"preset": "push", "intensity": 0.2},
                "composition": {
                    "coordinateSpace": {"width": 1280, "height": 720},
                    "nodes": [
                        {
                            "id": "paper-sun",
                            "kind": "asset",
                            "assetRole": "decorative",
                            "shape": "circle",
                            "fill": "#d56b37",
                            "z": 1,
                            "transform": {"x": 970, "y": 155, "width": 110, "height": 110, "anchorX": 0.5, "anchorY": 0.5},
                            "motion": {"keyframes": [{"at": 0, "scale": 0.9, "opacity": 0}, {"at": 0.28, "scale": 1, "opacity": 1}, {"at": 1, "scale": 1.03, "opacity": 1}]},
                        },
                        {
                            "id": "paper-ground",
                            "kind": "asset",
                            "assetRole": "environment",
                            "shape": "polygon",
                            "points": [[0, 510], [240, 430], [480, 535], [760, 410], [1030, 505], [1280, 430], [1280, 720], [0, 720]],
                            "fill": "#40352d",
                            "z": 2,
                            "transform": {"x": 0, "y": 0, "width": 1280, "height": 720, "anchorX": 0, "anchorY": 0},
                            "motion": {"keyframes": [{"at": 0, "y": 14}, {"at": 1, "y": 0}]},
                        },
                        {
                            "id": "paper-figure",
                            "kind": "group",
                            "pattern": "free",
                            "z": 4,
                            "coordinateSpace": {"width": 200, "height": 300},
                            "transform": {"x": 560, "y": 330, "width": 200, "height": 300, "anchorX": 0.5, "anchorY": 1},
                            "motion": {"keyframes": [{"at": 0, "x": -80, "opacity": 0}, {"at": 0.35, "x": 0, "opacity": 1}, {"at": 1, "x": 8, "opacity": 1}]},
                            "children": [
                                {"id": "torso", "kind": "asset", "assetRole": "character", "shape": "polygon", "points": [[70, 90], [130, 90], [155, 230], [45, 230]], "fill": "#d8c7a7", "z": 2, "transform": {"x": 0, "y": 0, "width": 200, "height": 300, "anchorX": 0, "anchorY": 0}, "motion": {"keyframes": [{"at": 0, "rotation": -2}, {"at": 1, "rotation": 2}]}},
                                {"id": "head", "kind": "asset", "assetRole": "character", "shape": "circle", "fill": "#d8c7a7", "z": 3, "transform": {"x": 100, "y": 58, "width": 64, "height": 64, "anchorX": 0.5, "anchorY": 0.5}, "motion": {"keyframes": [{"at": 0, "rotation": -4}, {"at": 0.55, "rotation": 5}, {"at": 1, "rotation": 1}]}},
                            ],
                        },
                    ],
                },
                "cues": [
                    {"id": "cue-establish", "beatId": "establish", "at": 0.12, "targetId": "scene-01", "action": "reveal", "intensity": 0.5, "proofTimeId": "establish"},
                    {"id": "cue-action", "beatId": "action", "at": 0.52, "targetId": "paper-figure", "action": "lift", "intensity": 0.5, "proofTimeId": "action"},
                    {"id": "cue-final", "beatId": "final", "at": 0.86, "targetId": "scene-01", "action": "settle", "intensity": 0.3, "proofTimeId": "final"},
                ],
                "proofTimes": storyboard["scenes"][0]["proofTimes"],
            }
        ],
    }
    write_json(project_dir / "project.json", project)
    write_json(project_dir / "semantic-contracts.json", {"schemaVersion": 1, "contracts": []})
    write_json(project_dir / "assets-manifest.json", {"schemaVersion": 1, "assets": []})
    write_json(project_dir / "quality-report.json", {"schemaVersion": 2, "assets": [], "composites": []})

    print(json.dumps({"workspace": str(target), "project": str(project_dir), "slug": slug}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
