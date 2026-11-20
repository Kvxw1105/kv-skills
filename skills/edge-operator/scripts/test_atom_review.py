#!/usr/bin/env python3
import copy
import json
import re
import unittest
from pathlib import Path
from atom_review import validate_registry,validate_trials,review,beta_prob_above_half

ROOT=Path(__file__).resolve().parent.parent
REG=json.loads((ROOT/'references/atom-registry.json').read_text(encoding='utf-8'))
RX=json.loads((ROOT/'references/research-atoms.json').read_text(encoding='utf-8'))['research_atoms']

class AtomReviewTests(unittest.TestCase):
    def test_registry_all_96_plus_16(self):
        legacy=set(re.findall(r'(?m)^- \*\*([A-L]\d{2})\s+', (ROOT/'references/mind-atoms.md').read_text(encoding='utf-8')))
        self.assertEqual(len(legacy),96)
        self.assertEqual(validate_registry(REG,legacy,RX),[])
        self.assertEqual(len(REG['atoms']),112)
        self.assertEqual(set(x['evidence_tier'] for x in REG['atoms']),{'heuristic','research_linked'})
    def test_default_has_no_fake_successes(self):
        summary=review({'trials':[]},REG)
        self.assertEqual(sum(a['all_trials'] for a in summary.values()),0)
        self.assertTrue(all(a['recommendation']=='collect_more_or_patch' for a in summary.values()))
    def test_beta_math(self):
        self.assertAlmostEqual(beta_prob_above_half(1,1),.5)
        self.assertAlmostEqual(beta_prob_above_half(2,1),.75)
        self.assertAlmostEqual(beta_prob_above_half(1,2),.25)
    def test_uncontrolled_observation_no_posterior_claim(self):
        t={'trial_id':'t1','atom_id':'A01','task_id':'task1','context_id':'one','design':'uncontrolled_observation',
           'treatment_success':True,'control_success':False,'treatment_receipt':'test:one','control_receipt':'test:two',
           'reviewed':True,'evaluator':'test','split':'heldout'}
        self.assertEqual(validate_trials({'trials':[t]}, {a['id'] for a in REG['atoms']}),[])
        result=review({'trials':[t]},REG)['A01']
        self.assertEqual(result['heldout_discordant'],0)
        self.assertEqual(result['recommendation'],'collect_more_or_patch')
    def test_duplicate_task_atom_rejected(self):
        t={'trial_id':'t1','atom_id':'A01','task_id':'same','context_id':'one','design':'randomized_paired',
           'treatment_success':True,'control_success':False,'treatment_receipt':'test:one','control_receipt':'test:two',
           'reviewed':True,'evaluator':'test','split':'heldout'}
        duplicate={**t,'trial_id':'t2'}
        self.assertTrue(any('duplicate task/atom pair' in e for e in validate_trials({'trials':[t,duplicate]},{'A01'})))
    def test_synthetic_success_never_auto_promotes(self):
        trials=[]
        for i in range(25):
            trials.append({'trial_id':f't{i}', 'atom_id':'A01', 'task_id':f'case{i}', 'context_id':f'group{i%5}',
                           'design':'randomized_paired','treatment_success':True,'control_success':False,
                           'treatment_receipt':f'test:treated{i}','control_receipt':f'test:control{i}',
                           'reviewed':True,'evaluator':'sandbox','split':'heldout'})
        r=review({'trials':trials},REG)['A01']
        self.assertEqual(r['recommendation'],'promotion_review_candidate')
        self.assertEqual(r['lifecycle'],'candidate')
        self.assertEqual(REG['atoms'][0]['lifecycle'],'candidate')

if __name__=='__main__':unittest.main()
