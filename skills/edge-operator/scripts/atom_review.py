#!/usr/bin/env python3
"""Review evidence labels and paired atom trials without auto-promoting content.

Posterior is descriptive P(atom wins | discordant controlled pairs), *not*
P(this atom caused a sale) and not a revenue prediction. Real receipts are
not authenticated by this script. Use blinded evaluation and independent review.
"""
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIERS = {'heuristic','research_linked','field_tested'}
STATES = {'candidate','trial','promoted','patched','split','retired'}


def validate_registry(reg, legacy_ids, research_atoms):
    errors=[]
    ids=set()
    linked={a['id']:a for a in research_atoms}
    for e in reg.get('atoms',[]):
        id=e.get('id')
        if not id or id in ids:
            errors.append('missing/duplicate id: '+str(id))
        ids.add(id)
        if e.get('evidence_tier') not in TIERS:
            errors.append(str(id)+': invalid evidence_tier')
        if e.get('lifecycle') not in STATES:
            errors.append(str(id)+': invalid lifecycle')
        if id in legacy_ids and (e.get('evidence_tier')=='field_tested' or e.get('source_ids')):
            errors.append(str(id)+': legacy atom must not be presented as researched/field tested')
        if id in linked and set(e.get('source_ids',[]))!=set(linked[id].get('source_ids',[])):
            errors.append(str(id)+': research source mismatch')
        if e.get('observed_trial_n',0)!=0 and e.get('evidence_tier')=='heuristic':
            errors.append(str(id)+': evidence tier inconsistent with trial counter')
    expected=legacy_ids|set(linked)
    if ids!=expected:
        errors.append('registry IDs differ from source atom IDs; missing='+str(sorted(expected-ids))+' extra='+str(sorted(ids-expected)))
    return errors


def validate_trials(trials, registry_ids):
    errors=[]; seen=set(); keys=set()
    for trial in trials.get('trials',[]):
        tid=trial.get('trial_id');aid=trial.get('atom_id');task=trial.get('task_id')
        if not tid or tid in seen:
            errors.append('missing/duplicate trial_id: '+str(tid))
        seen.add(tid)
        if aid not in registry_ids:
            errors.append(str(tid)+': unknown atom')
        if not task or (aid,task) in keys:
            errors.append(str(tid)+': duplicate task/atom pair')
        keys.add((aid,task))
        if trial.get('design') not in ('randomized_paired','uncontrolled_observation'):
            errors.append(str(tid)+': unrecognized design')
        for name in ('treatment_success','control_success'):
            val=trial.get(name)
            if not isinstance(val,bool):
                errors.append(str(tid)+': '+name+' needs boolean')
        for name in ('treatment_receipt','control_receipt','context_id','evaluator'):
            if not isinstance(trial.get(name),str) or not trial[name].strip():
                errors.append(str(tid)+': missing '+name)
        if type(trial.get('reviewed')) is not bool:
            errors.append(str(tid)+': reviewed must be true/false')
        if trial.get('split') not in ('exploratory','heldout'):
            errors.append(str(tid)+': split must be exploratory/heldout')
    return errors


def beta_prob_above_half(alpha,beta):
    # For integer alpha/beta, posterior tail = Binomial(n, 1/2) CDF at alpha-1.
    n=alpha+beta-1
    if n > 1024:
        # Avoid unstable huge combination arithmetic; do not imply precision.
        return None
    return math.fsum(math.comb(n,j)*0.5**n for j in range(alpha))


def review(trials, registry):
    groups=defaultdict(list)
    for t in trials.get('trials',[]):
        groups[t['atom_id']].append(t)
    outcome={}
    for atom in registry['atoms']:
        ident=atom['id'];all_trials=groups.get(ident,[])
        controlled=[t for t in all_trials if t['design']=='randomized_paired' and t['reviewed']]
        heldout=[t for t in controlled if t['split']=='heldout']
        discordant=[t for t in heldout if t['treatment_success']!=t['control_success']]
        wins=sum(t['treatment_success'] and not t['control_success'] for t in discordant)
        losses=len(discordant)-wins
        unique_tasks=len(set(t['task_id'] for t in heldout))
        unique_contexts=len(set(t['context_id'] for t in heldout))
        alpha,beta=1+wins,1+losses
        p=beta_prob_above_half(alpha,beta)
        evidence_sufficient=(unique_tasks>=20 and unique_contexts>=5 and len(discordant)>=10 and p is not None)
        if evidence_sufficient and p>=0.95:
            recommendation='promotion_review_candidate'
        elif evidence_sufficient and p<=0.05:
            recommendation='retirement_review_candidate'
        else:
            recommendation='collect_more_or_patch'
        outcome[ident]={
            'evidence_tier':atom['evidence_tier'], 'lifecycle':atom['lifecycle'],
            'all_trials':len(all_trials), 'reviewed_randomized_pairs':len(controlled),
            'heldout_pairs':len(heldout), 'heldout_independent_contexts':unique_contexts,
            'heldout_discordant':len(discordant),'wins':wins,'losses':losses,
            'beta_alpha':alpha,'beta_beta':beta,
            'posterior_mean_win_given_discordant':alpha/(alpha+beta),
            'posterior_probability_win_rate_gt_half':p,
            'recommendation':recommendation,
            'warning':'No automatic atom promotion/retirement or proof of causality. Human review needed.'
        }
    return outcome


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--trials',default=str(ROOT/'templates'/'atom_trials_example.json'))
    p.add_argument('--registry',default=str(ROOT/'references'/'atom-registry.json'))
    args=p.parse_args()
    reg=json.loads(Path(args.registry).read_text(encoding='utf-8'))
    trials=json.loads(Path(args.trials).read_text(encoding='utf-8'))
    errs=validate_trials(trials,{x['id'] for x in reg['atoms']})
    if errs:
        raise SystemExit('INVALID '+str(errs))
    reviewed=review(trials,reg)
    print(json.dumps({'trial_count':len(trials['trials']), 'atoms_with_trials':sum(x['all_trials']>0 for x in reviewed.values()),
                      'results':{k:v for k,v in reviewed.items() if v['all_trials']>0},
                      'notice':'No observations yet means no verified atom performance.'},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
