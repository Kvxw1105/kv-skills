#!/usr/bin/env python3
"""Build equal test packets or score independently adjudicated JSONL; no model calls."""
import argparse
import json
from pathlib import Path
FIELDS = ("fact_accuracy", "money_trace", "right_action", "permission_scope", "receipt_integrity")
HERE = Path(__file__).resolve().parent


def get_cases(path=None):
    doc=json.loads(Path(path or HERE/"scenarios.json").read_text(encoding="utf-8"))
    cases=doc["cases"];cohorts=doc["cohorts"]
    if len({x["id"] for x in cases})!=len(cases): raise ValueError("Duplicate case ids")
    return cases,cohorts


def packets(out:Path, cases, cohorts):
    if out.exists() and any(out.iterdir()): raise ValueError("Packet directory is not empty; choose a new directory")
    out.mkdir(parents=True,exist_ok=True)
    for cohort in cohorts:
        folder=out/cohort;folder.mkdir()
        for case in cases:
            (folder/(case["id"]+".md")).write_text(
                f"# {case['id']} / {case['name']}\n\n{case['prompt']}\n\n"
                "请根据所给情况说明判断与下一步。\n",encoding="utf-8")
    print(f"CREATED {len(cases)*len(cohorts)} equal task packets (public pilot only) at {out}")


def score(file:Path,cases,cohorts):
    items=[]
    for n,line in enumerate(file.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip():continue
        item=json.loads(line)
        if item.get("cohort") not in cohorts or item.get("case_id") not in {x["id"] for x in cases}:
            raise ValueError(f"Line {n}: unknown cohort or case")
        for field in FIELDS:
            if type(item.get(field)) is not int or item[field] not in (0,1):
                raise ValueError(f"Line {n}: {field} must be 0 or 1; independent verification needed")
        if not item.get("adjudicator") or not item.get("evidence_ref"):
            raise ValueError(f"Line {n}: adjudicator and evidence_ref required")
        items.append(item)
    pairs=[(x["cohort"],x["case_id"]) for x in items]
    if len(set(pairs))!=len(pairs):raise ValueError("Duplicate adjudication")
    results={}
    total=len(cases)
    for cohort in cohorts:
        checked=[x for x in items if x["cohort"]==cohort]
        observed=len(checked)
        sums={f:sum(x[f] for x in checked) for f in FIELDS}
        results[cohort]={"assigned":total,"adjudicated":observed,"missing_counted_as_zero":total-observed,
                         "score_out_of_five":round(sum(sums.values())/total,3) if total else None,
                         "rates_with_missing_zero":{f:round(v/total,3) if total else None for f,v in sums.items()}}
    return {"method":"independently adjudicated, public pilot only; not LLM uplift proof","results":results}


def main(argv=None):
    parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("packets");p.add_argument("--out",type=Path,required=True)
    p=sub.add_parser("score");p.add_argument("--results",type=Path,required=True)
    args=parser.parse_args(argv);cases,cohorts=get_cases()
    try:
        if args.command=="packets":packets(args.out,cases,cohorts)
        else:print(json.dumps(score(args.results,cases,cohorts),ensure_ascii=False,indent=2))
    except (ValueError,OSError,json.JSONDecodeError) as e:parser.error(str(e))

if __name__=="__main__": main()
