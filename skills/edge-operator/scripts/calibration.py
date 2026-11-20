#!/usr/bin/env python3
"""Auditable binary forecasts, frozen before settlement. Structural proof, not truth.

Commands:
  python scripts/calibration.py validate templates/forecast_example.json
  python scripts/calibration.py freeze path.json FORECAST_ID
  python scripts/calibration.py settle path.json FORECAST_ID 1 RECEIPT_URI
  python scripts/calibration.py report path.json

Only stdlib. Never treat the example as an observed customer outcome.
"""
import argparse
import copy
import hashlib
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

LOCKED_FIELDS = (
    'forecast_id', 'opportunity_id', 'question', 'outcome_definition',
    'population', 'settle_by', 'probability', 'falsifier', 'reference_class',
    'hypotheses', 'position', 'decay', 'atom_ids', 'evidence_plan'
)


def parse_date(value):
    return date.fromisoformat(value)


def parse_datetime(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('timezone required')
    return parsed.astimezone(timezone.utc)


def probability(p):
    return isinstance(p, (int, float)) and not isinstance(p, bool) and 0 <= p <= 1


def fingerprint(f):
    payload = json.dumps({key: f.get(key) for key in LOCKED_FIELDS},
                         sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def validate_forecast(f):
    errs = []
    ident = f.get('forecast_id', '<unnamed>')
    for k in ('forecast_id', 'opportunity_id', 'question', 'outcome_definition',
              'population', 'settle_by', 'falsifier', 'evidence_plan'):
        if not isinstance(f.get(k), str) or not f[k].strip():
            errs.append(f'{ident}: missing {k}')
    if not probability(f.get('probability')):
        errs.append(f'{ident}: numeric probability must be within [0,1]')
    try:
        parse_date(f.get('settle_by', ''))
    except (ValueError, TypeError):
        errs.append(f'{ident}: settle_by requires ISO YYYY-MM-DD')
    ref = f.get('reference_class')
    if not isinstance(ref, dict):
        errs.append(f'{ident}: reference_class missing')
    else:
        for k in ('description', 'selection_bias'):
            if not ref.get(k):
                errs.append(f'{ident}: reference_class missing {k}')
        n, wins, p = ref.get('sample_n'), ref.get('success_n'), ref.get('base_rate')
        if n is None:
            if wins is not None or p is not None:
                errs.append(f'{ident}: unknown cohort must not invent base_rate')
        else:
            if not isinstance(n, int) or isinstance(n, bool) or n < 1:
                errs.append(f'{ident}: cohort sample_n must be positive')
            elif not isinstance(wins, int) or isinstance(wins, bool) or not 0 <= wins <= n:
                errs.append(f'{ident}: cohort success_n invalid')
            elif not probability(p) or abs(p-wins/n)>1e-6:
                errs.append(f'{ident}: base_rate does not match sampled cohort')
            if not ref.get('source_ref') or not ref.get('as_of'):
                errs.append(f'{ident}: baseline cohort requires source_ref and as_of')
    hypotheses = f.get('hypotheses')
    if not isinstance(hypotheses, list) or len(hypotheses)<2:
        errs.append(f'{ident}: require >=2 competing hypotheses')
    else:
        seen = set()
        for h in hypotheses:
            if not isinstance(h, dict) or not h.get('id') or not h.get('disconfirming_test') or not h.get('explanation'):
                errs.append(f'{ident}: hypothesis requires id, explanation, disconfirming_test')
                continue
            if h['id'] in seen:
                errs.append(f'{ident}: duplicate hypothesis id')
            seen.add(h['id'])
    position, decay = f.get('position'), f.get('decay')
    for key, obj, fields in [
        ('position', position, ('bottleneck_owner','our_position','can_be_bypassed','value_capture')),
        ('decay', decay, ('why_gap_remains','erosion_trigger','recheck_on')),
    ]:
        if not isinstance(obj, dict) or any(obj.get(k) in (None,'') for k in fields):
            errs.append(f'{ident}: {key} incomplete, require {fields}')
    if isinstance(decay, dict):
        try:
            parse_date(decay.get('recheck_on',''))
        except (TypeError, ValueError):
            errs.append(f'{ident}: decay.recheck_on requires date')
    atoms = f.get('atom_ids')
    if not isinstance(atoms, list) or not atoms or not all(isinstance(x,str) for x in atoms):
        errs.append(f'{ident}: atom_ids must be nonempty IDs')
    state = f.get('state')
    if state not in ('DRAFT','FROZEN','SETTLED','VOID'):
        errs.append(f'{ident}: state must be DRAFT/FROZEN/SETTLED/VOID')
    elif state == 'DRAFT':
        if f.get('frozen_at') or f.get('forecast_sha256') or f.get('outcome') is not None:
            errs.append(f'{ident}: DRAFT must not contain frozen/outcome data')
    else:
        try:
            frozen = parse_datetime(f.get('frozen_at',''))
        except (ValueError, TypeError):
            frozen = None
            errs.append(f'{ident}: frozen_at invalid')
        if f.get('forecast_sha256') != fingerprint(f):
            errs.append(f'{ident}: frozen fingerprint mismatch (forecast mutated)')
        if state == 'FROZEN' and f.get('outcome') is not None:
            errs.append(f'{ident}: FROZEN must have no settlement')
        if state == 'VOID':
            if f.get('outcome') is not None:
                errs.append(f'{ident}: VOID must not have a scored outcome')
            v=f.get('void')
            if not isinstance(v,dict) or not v.get('reason') or not v.get('evidence_ref') or not v.get('voided_at'):
                errs.append(f'{ident}: VOID requires reason, evidence_ref, voided_at')
        if state == 'SETTLED':
            outcome = f.get('outcome')
            if not isinstance(outcome, dict) or outcome.get('value') not in (0,1) or type(outcome.get('value')) is not int:
                errs.append(f'{ident}: binary outcome must be 0 or 1')
            else:
                if not isinstance(outcome.get('evidence_ref'),str) or not outcome['evidence_ref'].strip():
                    errs.append(f'{ident}: settlement requires external evidence_ref')
                if not isinstance(outcome.get('adjudicator'),str) or not outcome['adjudicator'].strip():
                    errs.append(f'{ident}: settlement requires named adjudicator/review role')
                try:
                    resolved = parse_datetime(outcome.get('resolved_at',''))
                    if frozen and resolved < frozen:
                        errs.append(f'{ident}: settlement predates frozen forecast')
                except (ValueError, TypeError):
                    errs.append(f'{ident}: outcome.resolved_at invalid')
    return errs


def validate_book(book):
    errors = []
    if not isinstance(book.get('forecasts'),list):
        return ['forecasts must be a list']
    ids=set()
    for f in book['forecasts']:
        if not isinstance(f,dict):
            errors.append('forecast entry not an object')
            continue
        ident=f.get('forecast_id')
        if ident in ids:
            errors.append(f'duplicate forecast ID: {ident}')
        ids.add(ident)
        errors+=validate_forecast(f)
    return errors


def freeze(f, frozen_at=None):
    if f.get('state') != 'DRAFT':
        raise ValueError('freeze requires DRAFT')
    errs=validate_forecast(f)
    if errs:
        raise ValueError('; '.join(errs))
    f=copy.deepcopy(f)
    f['frozen_at']=(frozen_at or datetime.now(timezone.utc)).isoformat()
    f['forecast_sha256']=fingerprint(f)
    f['state']='FROZEN'
    return f


def settle(f, value, evidence_ref, adjudicator='human-review', resolved_at=None):
    if f.get('state')!='FROZEN':
        raise ValueError('settle requires FROZEN')
    if type(value) is not int or value not in (0,1):
        raise ValueError('outcome must be integer 0 or 1')
    if not evidence_ref or not adjudicator:
        raise ValueError('independent receipt and adjudicator required')
    if validate_forecast(f):
        raise ValueError('forecast invalid or edited after freeze')
    f=copy.deepcopy(f)
    f['state']='SETTLED'
    f['outcome']={'value':value,'evidence_ref':evidence_ref,'adjudicator':adjudicator,
                  'resolved_at':(resolved_at or datetime.now(timezone.utc)).isoformat()}
    errs=validate_forecast(f)
    if errs:
        raise ValueError('; '.join(errs))
    return f


def void_forecast(f, reason, evidence_ref):
    if f.get('state')!='FROZEN' or validate_forecast(f):
        raise ValueError('void requires unchanged FROZEN forecast')
    if not reason or not evidence_ref:
        raise ValueError('void requires reason and evidence')
    f=copy.deepcopy(f)
    f['state']='VOID'
    f['void']={'reason':reason,'evidence_ref':evidence_ref,'voided_at':datetime.now(timezone.utc).isoformat()}
    return f


def report(book, today=None):
    today=today or date.today()
    fs=book.get('forecasts',[])
    valid=[f for f in fs if not validate_forecast(f)]
    settled=[f for f in valid if f['state']=='SETTLED']
    scored=[((f['probability']-f['outcome']['value'])**2,f) for f in settled]
    paired=[((f['reference_class']['base_rate']-f['outcome']['value'])**2,(f['probability']-f['outcome']['value'])**2)
            for f in settled if f['reference_class'].get('base_rate') is not None]
    overdue=sum(1 for f in valid if f['state']=='FROZEN' and parse_date(f['settle_by'])<today)
    missing_baseline=sum(1 for f in settled if f['reference_class'].get('base_rate') is None)
    def average(values):
        return sum(values)/len(values) if values else None
    brier=average([b for b,_ in scored]); base=average([x for x,_ in paired]); pair=average([y for _,y in paired])
    return {
        'total':len(fs),'valid':len(valid),'invalid':len(fs)-len(valid),
        'draft':sum(f['state']=='DRAFT' for f in valid),
        'frozen_open':sum(f['state']=='FROZEN' for f in valid),
        'void_n':sum(f['state']=='VOID' for f in valid),
        'overdue_open':overdue,'settled_n':len(settled),
        'brier_mean':brier, 'paired_baseline_n':len(paired),
        'paired_baseline_brier':base,'paired_forecast_brier':pair,
        'brier_skill_vs_cohort':(1-pair/base) if base and base>0 else None,
        'settled_missing_baseline':missing_baseline,
        'judgment':'descriptive_only' if len(settled)<30 else 'needs_independence_and_confidence_checks',
        'warning':'A recorded receipt is not proof of authenticity; no causal atom attribution from these scores.'
    }


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('command',choices=('validate','freeze','settle','void','report'))
    p.add_argument('book',type=Path)
    p.add_argument('id',nargs='?')
    p.add_argument('value',nargs='?')
    p.add_argument('evidence',nargs='?')
    p.add_argument('--adjudicator',default='human-review')
    p.add_argument('--reason',default='predeclared outcome unavailable')
    args=p.parse_args(argv)
    book=json.loads(args.book.read_text(encoding='utf-8'))
    if args.command in ('freeze','settle','void'):
        if not args.id:
            p.error('forecast id required')
        matches=[i for i,f in enumerate(book['forecasts']) if f['forecast_id']==args.id]
        if len(matches)!=1:
            p.error('forecast id missing or duplicated')
        i=matches[0]
        try:
            book['forecasts'][i]=(freeze(book['forecasts'][i]) if args.command=='freeze' else
                                  void_forecast(book['forecasts'][i],args.reason,args.evidence or args.value) if args.command=='void' else
                                  settle(book['forecasts'][i],int(args.value),args.evidence,args.adjudicator))
        except (ValueError,TypeError) as exc:
            p.error(str(exc))
        if validate_book(book):
            p.error('book invalid: '+'; '.join(validate_book(book)))
        args.book.write_text(json.dumps(book,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.command=='validate':
        errors=validate_book(book)
        print(json.dumps({'pass':not errors,'errors':errors},ensure_ascii=False,indent=2))
        return 2 if errors else 0
    if args.command=='report':
        print(json.dumps(report(book),ensure_ascii=False,indent=2))
    if args.command in ('freeze','settle','void'):
        print(args.command.upper()+' '+args.id)
    return 0

if __name__=='__main__':
    sys.exit(main())
