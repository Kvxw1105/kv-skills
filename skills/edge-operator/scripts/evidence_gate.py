#!/usr/bin/env python3
"""Fail closed on evidence laundering; this validates claims, not source authenticity.

Usage: python scripts/evidence_gate.py examples/etsy-authenticity-2026/opportunity-evidence.json
Only the Python standard library is required.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = ROOT / 'references' / 'research-source-ledger.json'
ATOMS_PATH = ROOT / 'references' / 'research-atoms.json'

ALLOWED_SOURCE_TYPES = {
    'policy': {'platform_official', 'regulator_official'},
    'pain': {'community_testimony', 'practitioner_firsthand'},
    'adjacent_offer': {'marketplace_offer'},
    'buyer_commitment': {'buyer_confirmation', 'verified_transaction'},
    'confirmed_payment': {'verified_transaction'},
}


def sources_by_id(ledger):
    return {item['id']: item for item in ledger['sources']}


def check_atoms(atoms_data, ledger):
    errors = []
    atoms = atoms_data.get('research_atoms', [])
    seen = set()
    srcs = sources_by_id(ledger)
    for atom in atoms:
        aid = atom.get('id')
        if not aid or aid in seen:
            errors.append('duplicate or missing atom id: ' + str(aid))
        seen.add(aid)
        for key in ('name', 'trigger', 'question', 'observable', 'decision_rule', 'next_action', 'falsifier'):
            if not isinstance(atom.get(key), str) or len(atom[key].strip()) < 6:
                errors.append('%s: missing meaningful %s' % (aid, key))
        if not atom.get('source_ids'):
            errors.append('%s: no source_ids' % aid)
        for s in atom.get('source_ids', []):
            if s not in srcs:
                errors.append('%s: unknown source %s' % (aid, s))
    return errors


def evaluate_case(case, ledger, forecast_book=None):
    """Returns (errors, summary), never infers payment from offers/complaints."""
    errors = []
    srcs = sources_by_id(ledger)
    kinds = set()
    for i, obs in enumerate(case.get('observations', []), 1):
        kind = obs.get('kind')
        src_ids = obs.get('source_ids', [])
        if not isinstance(obs.get('statement'), str) or not obs.get('statement').strip():
            errors.append('observation %d missing statement' % i)
        if kind != 'offer_hypothesis' and not src_ids:
            errors.append('observation %d missing sources' % i)
        good = []
        for sid in src_ids:
            if sid not in srcs:
                errors.append('observation %d unknown source: %s' % (i, sid))
            else:
                good.append(srcs[sid]['kind'])
        if kind in ALLOWED_SOURCE_TYPES and not (set(good) & ALLOWED_SOURCE_TYPES[kind]):
            errors.append('observation %d %s lacks appropriate source kind' % (i, kind))
        if kind not in ALLOWED_SOURCE_TYPES and kind != 'offer_hypothesis':
            errors.append('observation %d unknown kind %s' % (i, kind))
        if kind == 'confirmed_payment' and not obs.get('receipt'):
            errors.append('observation %d payment lacks independent receipt' % i)
        kinds.add(kind)

    money = case.get('money', {})
    revenue = money.get('confirmed_revenue_usd', 0)
    if not isinstance(revenue, (int, float)) or isinstance(revenue, bool) or revenue < 0:
        errors.append('confirmed revenue must be nonnegative numeric')
    elif revenue > 0 and ('confirmed_payment' not in kinds or not money.get('payment_receipt')):
        errors.append('revenue asserted without payment evidence')
    if money.get('pricing_status') not in ('hypothesis', 'offer_observed', 'paid_verified'):
        errors.append('pricing_status must be hypothesis/offer_observed/paid_verified')
    if money.get('pricing_status') == 'paid_verified' and not money.get('payment_receipt'):
        errors.append('paid_verified pricing lacks receipt')

    action = case.get('action', {})
    if action.get('status') not in ('prepared', 'executed', 'blocked', 'not_started'):
        errors.append('invalid action status')
    elif action.get('status') == 'executed' and not action.get('receipt'):
        errors.append('execution asserted without tool/action receipt')
    if not case.get('stop_condition'):
        errors.append('must state falsifiable stop condition')
    if not case.get('hypothesis'):
        errors.append('must state business hypothesis')

    decision_mode=case.get('decision_mode','exploratory')
    if decision_mode not in ('exploratory','actionable'):
        errors.append('unknown decision_mode')
    if decision_mode=='actionable':
        from calibration import validate_forecast
        fid=case.get('forecast_id')
        candidates=[f for f in forecast_book.get('forecasts',[]) if f.get('forecast_id')==fid] if isinstance(forecast_book,dict) else []
        if not fid or len(candidates)!=1:
            errors.append('actionable decision requires one frozen forecast record')
        else:
            f=candidates[0]
            if f.get('state') not in ('FROZEN','SETTLED') or validate_forecast(f) or f.get('opportunity_id')!=case.get('case_id'):
                errors.append('actionable forecast must be frozen, valid and linked to case ID')

    stage = ('PAID_EVIDENCE_PRESENT' if 'confirmed_payment' in kinds and money.get('payment_receipt') else
             'POLICY_PAIN_OFFER_NO_PAYMENT' if {'policy','pain','adjacent_offer'} <= kinds else
             'EARLY_EVIDENCE_ONLY')
    return errors, {'case_id':case.get('case_id'), 'stage':stage,
                    'verified_revenue_usd':revenue if stage=='PAID_EVIDENCE_PRESENT' and not errors else 0,
                    'next_evidence_needed':'Verified payment or deposit and unit economics after actual seller contact' if stage!='PAID_EVIDENCE_PRESENT' else 'True costs, refunds, repeat business',
                    'action_status':action.get('status')}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('case_file', type=Path)
    p.add_argument('--json', action='store_true')
    args = p.parse_args(argv)
    ledger = json.loads(SOURCE_PATH.read_text(encoding='utf-8'))
    atoms = json.loads(ATOMS_PATH.read_text(encoding='utf-8'))
    case = json.loads(args.case_file.read_text(encoding='utf-8'))
    book=None
    if case.get('decision_mode')=='actionable':
        ref=case.get('forecast_book')
        if isinstance(ref,str) and ref and not Path(ref).is_absolute():
            fp=(ROOT/ref).resolve()
            if fp.is_relative_to(ROOT) and fp.is_file() and fp.suffix=='.json':
                try:book=json.loads(fp.read_text(encoding='utf-8'))
                except (ValueError,OSError):pass
    errors,summary = evaluate_case(case,ledger,book)
    errors.extend(check_atoms(atoms, ledger))
    result={'pass':not errors,'errors':errors,'summary':summary,
            'source_count':len(ledger['sources']),'research_atom_count':len(atoms['research_atoms'])}
    print(json.dumps(result,indent=2,ensure_ascii=False) if args.json else
          'PASS' if not errors else 'FAIL: '+ '; '.join(errors))
    return 0 if not errors else 2

if __name__ == '__main__':
    sys.exit(main())
