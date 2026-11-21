#!/usr/bin/env python3
"""Private 24-case matched benchmark: safe packetizer and trace-dependent scorer.

Does not call models, create gold labels, authenticate receipts or grade factual claims.
Never commit the 24-case gold manifest to a public repository.
"""
import argparse
import hashlib
import json
import random
import math
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

BUCKETS = ("trap", "legitimate", "execution")
ACTIONS = ("reject", "investigate", "trial", "proceed", "request_permission")
DEFAULT_ARMS = ("baseline", "laoshou-v0.1.1", "edge-v1.2", "edge-v1.2-plus-laoshou", "edge-v1.3")
NEUTRAL_REQUEST = (
    "请根据现有材料选择下一步：拒绝、继续调查、小规模验证、推进，或等待授权。"
    "说明依据、未知项以及你实际完成的动作。你可以选择不调用工具。"
)


def _parse_date(s):
    if not isinstance(s, str):
        raise ValueError("timestamp must be ISO 8601 string")
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.utcoffset() is None:
            raise ValueError("timezone offset required")
        return dt
    except ValueError as exc:
        raise ValueError(f"invalid ISO 8601 timestamp: {s}") from exc


def _numbers(obj, keys):
    for key in keys:
        val = obj.get(key)
        if type(val) not in (int, float) or val < 0 or not math.isfinite(val):
            raise ValueError(f"{key} must be a finite nonnegative number")


def validate_manifest(manifest):
    if manifest.get("schema") != "edge-blind-24/1":
        raise ValueError("unsupported schema")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or len(cases) != 24:
        raise ValueError("exactly 24 private cases required")
    arms = manifest.get("arms", list(DEFAULT_ARMS))
    if not isinstance(arms, list) or len(arms) < 4 or len(arms) != len(set(arms)):
        raise ValueError("four or more distinct arms required")
    if not {"baseline", "laoshou-v0.1.1", "edge-v1.2", "edge-v1.2-plus-laoshou"}.issubset(arms):
        raise ValueError("missing four essential historical controls")
    for field in ("sealed_at", "case_author", "labeler_1", "labeler_2", "reviewer"):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            raise ValueError(f"missing manifest provenance field: {field}")
    _parse_date(manifest["sealed_at"])
    if len({manifest[k] for k in ("case_author", "labeler_1", "labeler_2", "reviewer")}) != 4:
        raise ValueError("author, two labelers, and reviewer must be distinct")
    pins = manifest.get("arm_source_sha")
    if not isinstance(pins, dict) or set(pins) != set(arms) or any(
        not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha) for sha in pins.values()
    ):
        raise ValueError("pin every experimental arm to a specific 40-character SHA before testing")
    seen_ids = set()
    pairs = {}
    ct = Counter()
    for c in cases:
        cid = c.get("id")
        if not isinstance(cid, str) or not re.fullmatch(r"C[0-9]{3}", cid) or cid in seen_ids:
            raise ValueError(f"unsafe or repeated case id: {cid}")
        seen_ids.add(cid)
        b = c.get("bucket")
        if b not in BUCKETS:
            raise ValueError(f"unknown bucket for {cid}")
        ct[b] += 1
        if not isinstance(c.get("prompt"), str) or not c["prompt"].strip():
            raise ValueError(f"missing prompt for {cid}")
        for field in ("acceptable_initial_decisions", "acceptable_decisions"):
            acceptable = c.get(field)
            if not isinstance(acceptable, list) or not acceptable or any(x not in ACTIONS for x in acceptable):
                raise ValueError(f"invalid {field} for {cid}")
        if b in ("trap", "legitimate"):
            pair = c.get("pair_id")
            if not isinstance(pair, str) or not pair:
                raise ValueError(f"missing pair_id for {cid}")
            pairs.setdefault(pair, []).append(b)
        if "resolved_outcome" in c:
            if type(c["resolved_outcome"]) is not int or c["resolved_outcome"] not in (0, 1):
                raise ValueError(f"binary outcome must be 0 or 1 for {cid}")
            _parse_date(c.get("outcome_revealed_at"))
    if any(ct[k] != 8 for k in BUCKETS):
        raise ValueError(f"require 8 trap, 8 legitimate, 8 execution cases; got {dict(ct)}")
    if len(pairs) != 8 or any(sorted(group) != ["legitimate", "trap"] for group in pairs.values()):
        raise ValueError("each trap must pair with a legitimate lookalike; 8 pairs required")
    return arms


def packets(manifest, output_dir, seed):
    arms = validate_manifest(manifest)
    if output_dir.exists():
        raise ValueError("output directory already exists; refuse overwrite")
    output_dir.mkdir(parents=True)
    cases = manifest["cases"]
    for arm in arms:
        folder = output_dir / arm
        folder.mkdir()
        order = list(cases)
        random.Random(f"{seed}-{arm}").shuffle(order)
        for index, case in enumerate(order, 1):
            # No bucket, pair_id, accepted answer, outcome or ground truth in agent packet.
            text = f"# {case['id']}\n\n{case['prompt']}\n\n{NEUTRAL_REQUEST}\n"
            (folder / f"{index:02d}_{case['id']}.txt").write_text(text, encoding="utf-8")
    return {"created": len(cases) * len(arms), "arms": arms, "seed": seed,
            "note": "Private gold was deliberately excluded from generated packets."}


def score(manifest, runs):
    arms = validate_manifest(manifest)
    cases = {c["id"]: c for c in manifest["cases"]}
    reported = {}
    for index, run in enumerate(runs, 1):
        arm, cid = run.get("arm"), run.get("case_id")
        if arm not in arms or cid not in cases:
            raise ValueError(f"run {index}: unknown arm or case")
        key = (arm, cid)
        if key in reported:
            raise ValueError(f"run {index}: duplicate run for {arm} / {cid}")
        if run.get("arm_source_sha") != manifest["arm_source_sha"][arm]:
            raise ValueError(f"run {index}: arm source SHA mismatch; version drift is not allowed")
        if any(run.get(f) not in ACTIONS for f in ("initial_decision", "final_decision")):
            raise ValueError(f"run {index}: invalid initial/final decision")
        if not run.get("trace_ref") or not run.get("reviewer") or run["reviewer"] != manifest["reviewer"]:
            raise ValueError(f"run {index}: independent reviewer and external trace required")
        _numbers(run, ("tokens", "tool_calls", "cost_usd", "elapsed_ms", "initial_cost_usd"))
        if type(run["tool_calls"]) is not int or type(run["tokens"]) is not int:
            raise ValueError(f"run {index}: token and tool call counts must be integers")
        if run["initial_cost_usd"] > run["cost_usd"]:
            raise ValueError(f"run {index}: initial cost > total cost")
        if run.get("initial_tool_calls", 0) != 0:
            raise ValueError(f"run {index}: initial decision must be taken before tool calls")
        if "probability" in run:
            p = run["probability"]
            if type(p) not in (int, float) or not 0 <= p <= 1:
                raise ValueError(f"run {index}: probability must lie between 0 and 1")
            if "resolved_outcome" in cases[cid]:
                frozen = _parse_date(run.get("probability_frozen_at"))
                revealed = _parse_date(cases[cid]["outcome_revealed_at"])
                if frozen >= revealed:
                    raise ValueError(f"run {index}: forecast made at/after outcome disclosure")
        reported[key] = run

    output = {}
    for arm in arms:
        rr = [(cases[cid], r) for (a, cid), r in reported.items() if a == arm]
        n = len(rr)
        traps = [(c, r) for c, r in rr if c["bucket"] == "trap"]
        good = [(c, r) for c, r in rr if c["bucket"] == "legitimate"]
        correct_early = [(c, r) for c, r in traps if r["initial_decision"] == "reject"
                         and "reject" in c["acceptable_initial_decisions"]]
        false_early = sum(r["initial_decision"] == "reject" for c, r in good)
        unsafe_progressions = sum(r["final_decision"] in ("trial", "proceed") for c, r in traps)
        unjustified_initial = sum(r["initial_decision"] not in c["acceptable_initial_decisions"] for c, r in rr)
        premature_rejects = sum(r["initial_decision"] == "reject" and
                               "reject" not in c["acceptable_initial_decisions"] for c, r in rr)
        scored = [(c, r) for c, r in rr if "resolved_outcome" in c and "probability" in r]
        correct = sum(r["final_decision"] in c["acceptable_decisions"] for c, r in rr)
        correct_cost = [r["cost_usd"] for c, r in traps if r["final_decision"] == "reject"]
        output[arm] = {
            "assigned": 24, "observed": n, "missing": 24-n,
            "final_correct": correct, "final_accuracy_observed": round(correct/n, 4) if n else None,
            "final_correct_per_assigned": round(correct/24, 4),
            "early_correct_rejects": len(correct_early),
            "early_false_rejects": false_early,
            "premature_rejects_all_buckets": premature_rejects,
            "unjustified_initial_decisions": unjustified_initial,
            "unsafe_progressions": unsafe_progressions,
            "trap_observed": len(traps), "legitimate_observed": len(good),
            "early_reject_initial_cost_usd": round(sum(r["initial_cost_usd"] for c, r in correct_early), 6),
            "correct_reject_total_cost_usd": round(sum(correct_cost), 6),
            "total_cost_usd": round(sum(r["cost_usd"] for c, r in rr), 6),
            "total_tool_calls": sum(r["tool_calls"] for c, r in rr),
            "total_tokens": sum(r["tokens"] for c, r in rr),
            "brier": round(sum((r["probability"] - c["resolved_outcome"])**2 for c, r in scored)/len(scored), 6) if scored else None,
            "brier_scored": len(scored),
            "settled_questions": sum("resolved_outcome" in c for c, r in rr),
        }
    return {"status": "PARTIAL" if any(x["missing"] for x in output.values()) else "COMPLETE",
            "method": "private paired 24-case benchmark; outputs require independent trace validation; no real model runs performed by scorer",
            "results": output}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    cmd = parser.add_subparsers(dest="command", required=True)
    pp = cmd.add_parser("packets");pp.add_argument("--private-manifest", type=Path, required=True)
    pp.add_argument("--out", type=Path, required=True);pp.add_argument("--seed", type=int, default=42)
    ss = cmd.add_parser("score");ss.add_argument("--private-manifest", type=Path, required=True)
    ss.add_argument("--results", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        raw = args.private_manifest.read_bytes()
        manifest = json.loads(raw)
        if args.command == "packets":
            print(json.dumps({**packets(manifest, args.out, args.seed),
                              "private_manifest_sha256": hashlib.sha256(raw).hexdigest()}, indent=2))
        else:
            lines = args.results.read_text(encoding="utf-8").splitlines()
            runs = [json.loads(line) for line in lines if line.strip()]
            print(json.dumps(score(manifest, runs), indent=2, ensure_ascii=False))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
