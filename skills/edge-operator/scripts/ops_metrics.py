#!/usr/bin/env python3
"""Transparent process metrics with explicit denominators and missingness."""
import argparse
import json
from datetime import date
from pathlib import Path


def metrics(data):
    reviews=data.get('gate_reviews',[])
    # only independently adjudicated decisions (not all unreviewed blocks)
    adjudicated=[r for r in reviews if r.get('adjudication') in ('claim_valid','claim_invalid')]
    valid=[r for r in adjudicated if r['adjudication']=='claim_valid']
    false_blocks=sum(r.get('gate_decision')=='block' for r in valid)
    score_fpr=(false_blocks/len(valid)) if valid else None
    incidents=data.get('falsifications',[])
    resolved=[];unresolved=0
    for i in incidents:
        detected=i.get('disproof_detected_on');reversed_on=i.get('decision_corrected_on')
        if detected and reversed_on:
            delta=(date.fromisoformat(reversed_on)-date.fromisoformat(detected)).days
            if delta < 0:
                raise ValueError('decision corrected before disproof detection')
            resolved.append(delta)
        elif detected:
            unresolved+=1
    wins=data.get('successful_outcomes',[])
    codings=[x.get('luck_annotation') for x in wins]
    if any(c not in ('contributed','not_observed','unknown') for c in codings):
        raise ValueError('invalid luck_annotation')
    known=[c for c in codings if c!='unknown']
    annotated=sum(c=='contributed' for c in known)
    return {
        'falsification_delay_days_mean':sum(resolved)/len(resolved) if resolved else None,
        'falsification_delay_closed_n':len(resolved), 'falsification_delay_unresolved_n':unresolved,
        'gate_false_block_rate_on_independently_reviewed_valid_cases':score_fpr,
        'gate_valid_cases_reviewed_n':len(valid),'gate_all_reviewed_n':len(adjudicated),
        'luck_marked_contributing_fraction_among_known_annotations':annotated/len(known) if known else None,
        'luck_annotations_known_n':len(known),'luck_annotations_unknown_n':len(wins)-len(known),
        'warning':'Luck annotation is subjective, not an estimated causal fraction of profits. Review selection bias can distort error rates.'
    }


def main():
    p=argparse.ArgumentParser();p.add_argument('file',type=Path);args=p.parse_args()
    data=json.loads(args.file.read_text(encoding='utf-8'))
    print(json.dumps(metrics(data),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
