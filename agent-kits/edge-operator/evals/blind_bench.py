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
DEFAULT_ARMS = ("baseline", "laoshou-v0.1.2", "edge-v1.2", "edge-v1.2-plus-laoshou-v0.1.2", "edge-v1.3")
# Immutable public releases used in this trial. Changes require a new preregistered protocol.
PINNED_COMPONENT_REFS = {
    "baseline": {},
    "laoshou-v0.1.2": {"laoshou": "9a7fc5fb00851e4b406d288d81af561afe624bf5"},
    "edge-v1.2": {"edge": "22dd373c151acb426124b6cd8506beb4ce1cbffc"},
    "edge-v1.2-plus-laoshou-v0.1.2": {
        "edge": "22dd373c151acb426124b6cd8506beb4ce1cbffc",
        "laoshou": "9a7fc5fb00851e4b406d288d81af561afe624bf5",
    },
    "edge-v1.3": {"edge": "3b8b30e4d1125ff55ef96ec25b9a098229916f6d"},
}
NEUTRAL_REQUEST = (
    "阶段一：仅基于题面现有信息，不调用任何外部工具。先选择下一步：拒绝、继续调查、"
    "小规模验证、推进，或等待授权，并简要说明依据及未知项。请停在第一阶段答复。"
)
SECOND_STAGE_REQUEST = (
    "阶段二：现在可在同等授权、工具及成本预算下继续核查；提供最后的动作选择、"
    "已取得的可观察证据及仍未执行的部分。请区分已完成操作与尚未完成操作。"
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
    if not set(DEFAULT_ARMS).issubset(arms):
        raise ValueError("all five locked comparison arms must be present; do not silently reuse obsolete Laoshou v0.1.1")
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
    components = manifest.get("arm_components")
    if not isinstance(components, dict) or any(components.get(k) != v for k, v in PINNED_COMPONENT_REFS.items()):
        raise ValueError("arm_components must pin exact historical Laoshou v0.1.2 / Edge v1.2 and fused Edge v1.3 sources")
    seen_ids = set()
    pairs = {}
    ct = Counter()
    eligible_traps = set()
    zero_paid_legitimate = set()
    single_source_by_pair = {}
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
        if b == "trap":
            if type(c.get("distribution_clue_in_prompt")) is not bool:
                raise ValueError(f"{cid}: preregister distribution_clue_in_prompt as true/false")
            if c["distribution_clue_in_prompt"]:
                eligible_traps.add(c.get("pair_id"))
        if b == "legitimate":
            if type(c.get("no_paid_evidence_in_prompt")) is not bool:
                raise ValueError(f"{cid}: preregister no_paid_evidence_in_prompt as true/false")
            if c["no_paid_evidence_in_prompt"]:
                zero_paid_legitimate.add(c.get("pair_id"))
        if b in ("trap", "legitimate"):
            if type(c.get("single_source_material")) is not bool:
                raise ValueError(f"{cid}: preregister single_source_material as true/false")
            pair = c.get("pair_id")
            if pair in single_source_by_pair and single_source_by_pair[pair] != c["single_source_material"]:
                raise ValueError(f"{cid}: both sides of matched pair must share source-count condition")
            single_source_by_pair[pair] = c["single_source_material"]
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
    if len(eligible_traps & zero_paid_legitimate) < 3:
        raise ValueError("preregister at least 3 matched pairs with a trap-side visible distribution cue and legitimate-side no paid evidence")
    if sum(single_source_by_pair.get(pair, False) for pair in eligible_traps & zero_paid_legitimate) < 2:
        raise ValueError("include at least 2 eligible matched pairs built around a single promoter/link, not only viral multi-account hype")
    return arms


def packets(manifest, output_dir, seed):
    arms = validate_manifest(manifest)
    if output_dir.exists():
        raise ValueError("output directory already exists; refuse overwrite")
    output_dir.mkdir(parents=True)
    cases = manifest["cases"]
    (output_dir / "PHASE2.txt").write_text(SECOND_STAGE_REQUEST+"\n",encoding="utf-8")
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
        _numbers(run, ("tokens", "tool_calls", "cost_usd", "elapsed_ms", "initial_cost_usd", "initial_tokens", "initial_elapsed_ms"))
        if any(type(run[field]) is not int for field in ("tool_calls", "tokens", "initial_tokens", "initial_elapsed_ms")):
            raise ValueError(f"run {index}: token counts, calls and first-pass latency must be integers")
        for field in ("initial_distribution_named", "initial_downranked", "distribution_caused_reject"):
            if type(run.get(field)) is not bool:
                raise ValueError(f"run {index}: independent reviewer must provide boolean {field}")
        if run["initial_downranked"] and run["initial_decision"] not in ("reject", "investigate"):
            raise ValueError(f"run {index}: downranking needs an actual reject/investigate initial decision")
        if run["distribution_caused_reject"] and not (run["initial_distribution_named"] and run["initial_decision"] == "reject"):
            raise ValueError(f"run {index}: a distribution-caused rejection must name distribution and reject")
        if run["initial_tokens"] > run["tokens"] or run["initial_elapsed_ms"] > run["elapsed_ms"]:
            raise ValueError(f"run {index}: first-pass resource usage exceeds total")
        if run["initial_cost_usd"] > run["cost_usd"]:
            raise ValueError(f"run {index}: initial cost > total cost")
        if run.get("initial_tool_calls") != 0:
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
    # P1/P2/P3 are preregistered comparisons, NOT generalization claims. A few
    # matched cases can reject a brittle rule but cannot establish population accuracy.
    all_complete = all(output[a]["missing"] == 0 for a in DEFAULT_ARMS)
    b = "laoshou-v0.1.2"
    c = "edge-v1.2"
    trap_ids = [case_id for case_id, case in cases.items() if case["bucket"] == "trap" and case["distribution_clue_in_prompt"]]
    legit_ids = [case_id for case_id, case in cases.items() if case["bucket"] == "legitimate" and case["no_paid_evidence_in_prompt"]]
    single_trap_ids = [cid for cid in trap_ids if cases[cid]["single_source_material"]]
    def eligible(arm, ids):
        return [(cases[cid], reported[(arm, cid)]) for cid in ids if (arm, cid) in reported]
    def p1_hits(arm):
        return sum(r["initial_distribution_named"] and r["initial_downranked"]
                   and r["initial_decision"] in k["acceptable_initial_decisions"]
                   for k, r in eligible(arm, trap_ids))
    def ratio(num, den):
        return round(num / den, 6) if den > 0 else None
    a_hits, c_hits = p1_hits(b), p1_hits(c)
    a_rate, c_rate = ratio(a_hits, len(trap_ids)), ratio(c_hits, len(trap_ids))
    p1_gap = round(a_rate - c_rate, 6)
    p1_status = "PENDING"
    if all_complete:
        if c_rate >= 0.80 or p1_gap < 0.15:
            p1_status = "REFUTED"
        elif a_rate >= 0.80 and c_rate <= 0.50 and p1_gap >= 0.15:
            p1_status = "PILOT_SUPPORTED"
        else:
            p1_status = "NOT_SUPPORTED"
    # Initial stages have zero tools by design; paid first-pass cost includes prompt
    # prefill and output billing. Tokens and latency are separate diagnostics.
    a_cost = sum(r["initial_cost_usd"] for _, r in eligible(b, trap_ids))
    c_cost = sum(r["initial_cost_usd"] for _, r in eligible(c, trap_ids))
    cost_ratio = ratio(a_cost, c_cost) if all_complete else None
    a_tokens = sum(r["initial_tokens"] for _, r in eligible(b, trap_ids))
    c_tokens = sum(r["initial_tokens"] for _, r in eligible(c, trap_ids))
    token_ratio = ratio(a_tokens, c_tokens) if all_complete else None
    a_latency = sum(r["initial_elapsed_ms"] for _, r in eligible(b, trap_ids))
    c_latency = sum(r["initial_elapsed_ms"] for _, r in eligible(c, trap_ids))
    latency_ratio = ratio(a_latency, c_latency) if all_complete else None
    if cost_ratio is None:
        p2_status = "INCONCLUSIVE" if all_complete else "PENDING"
    elif cost_ratio <= 1/3:
        p2_status = "PILOT_SUPPORTED"
    elif cost_ratio > 1/2:
        p2_status = "REFUTED"
    else:
        p2_status = "GRAY_ZONE"
    p3_false_kills = sum(r["distribution_caused_reject"] for _, r in eligible(b, legit_ids))
    p3_status = ("PENDING" if not all_complete else
                 "REFUTED" if p3_false_kills >= 1 else "ZERO_OBSERVED_NOT_PROVEN")
    hypotheses = {
        "pilot_only": True,
        "p1_distribution_salience": {"status": p1_status, "eligible_trap_cases": len(trap_ids),
            "single_source_eligible_traps": len(single_trap_ids),
            "laoshou_hit_count": a_hits, "edge_v12_hit_count": c_hits,
            "laoshou_rate": a_rate if all_complete else None,
            "edge_v12_rate": c_rate if all_complete else None,
            "rate_difference": p1_gap if all_complete else None,
            "single_source_hits": {
                b: sum(r["initial_distribution_named"] and r["initial_downranked"] and
                       r["initial_decision"] in k["acceptable_initial_decisions"] for k, r in eligible(b, single_trap_ids)),
                c: sum(r["initial_distribution_named"] and r["initial_downranked"] and
                       r["initial_decision"] in k["acceptable_initial_decisions"] for k, r in eligible(c, single_trap_ids)),
            },
            "criteria": "pilot supported only if B >=80%, C <=50%, gap >=15pp; refuted if C >=80% or gap <15pp; otherwise not supported"},
        "p2_first_pass_cost": {"status": p2_status, "eligible_trap_cases": len(trap_ids),
            "laoshou_cost_usd": round(a_cost, 6) if all_complete else None,
            "edge_v12_cost_usd": round(c_cost, 6) if all_complete else None,
            "cost_ratio": cost_ratio, "initial_token_ratio": token_ratio,
            "initial_latency_ratio": latency_ratio,
            "criteria": "<=1/3 pilot supported; >1/2 refuted; intermediate gray zone; zero denominator inconclusive; both tool calls 0 in first pass"},
        "p3_no_distribution_false_kill": {"status": p3_status, "eligible_legitimate_cases": len(legit_ids),
            "false_kills_attributed_to_distribution": p3_false_kills,
            "criteria": ">=1 attributed false reject refutes pilot zero-error claim; zero cases does not establish universal zero-error rate"},
    }
    return {"status": "PARTIAL" if not all_complete else "COMPLETE",
            "method": "private paired 24-case benchmark; P1/P2/P3 exploratory preregistered thresholds; independent trace validation required; no real model runs by scorer",
            "hypotheses": hypotheses, "results": output}


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
