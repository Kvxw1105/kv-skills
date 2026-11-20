#!/usr/bin/env python3
"""Regression tests for source and money-truth gate, not an LLM benchmark."""
import copy
import json
import unittest
from pathlib import Path
from evidence_gate import evaluate_case, check_atoms
from calibration import freeze

ROOT=Path(__file__).resolve().parent.parent
LEDGER=json.loads((ROOT/'references/research-source-ledger.json').read_text(encoding='utf-8'))
ATOMS=json.loads((ROOT/'references/research-atoms.json').read_text(encoding='utf-8'))
CASE=json.loads((ROOT/'examples/etsy-authenticity-2026/opportunity-evidence.json').read_text(encoding='utf-8'))

class ResearchGateTests(unittest.TestCase):
    def test_source_integrity(self):
        self.assertEqual(len(LEDGER['sources']),len(set(s['id'] for s in LEDGER['sources'])))
        self.assertTrue(all(s['url'].startswith('https://') for s in LEDGER['sources']))
        self.assertTrue(all(s['caveat'] and s['claim_supported'] for s in LEDGER['sources']))
    def test_research_atom_integrity(self):
        self.assertEqual(check_atoms(ATOMS,LEDGER),[])
    def test_etsy_case_is_hypothesis_not_paid(self):
        errors,summary=evaluate_case(CASE,LEDGER)
        self.assertEqual(errors,[])
        self.assertEqual(summary['stage'],'POLICY_PAIN_OFFER_NO_PAYMENT')
        self.assertEqual(summary['verified_revenue_usd'],0)
    def test_offer_cannot_prove_payment(self):
        t=copy.deepcopy(CASE)
        t['money']['confirmed_revenue_usd']=39
        errors,_=evaluate_case(t,LEDGER)
        self.assertIn('revenue asserted without payment evidence',errors)
    def test_unpaid_offer_cannot_be_labeled_paid(self):
        t=copy.deepcopy(CASE)
        t['money']['pricing_status']='paid_verified'
        errors,_=evaluate_case(t,LEDGER)
        self.assertIn('paid_verified pricing lacks receipt',errors)
    def test_reddit_alone_cannot_prove_policy(self):
        t=copy.deepcopy(CASE)
        t['observations'][0]['source_ids']=['SRC16','SRC17']
        errors,_=evaluate_case(t,LEDGER)
        self.assertTrue(any('lacks appropriate source kind' in e for e in errors))
    def test_fiverr_offer_cannot_prove_buyer_commitment(self):
        t=copy.deepcopy(CASE)
        t['observations'].append({'kind':'buyer_commitment','statement':'already paid','source_ids':['SRC18']})
        errors,_=evaluate_case(t,LEDGER)
        self.assertTrue(any('buyer_commitment lacks appropriate source kind' in e for e in errors))
    def test_missing_source_blocked(self):
        t=copy.deepcopy(CASE)
        t['observations'][1]['source_ids']=['SRC999']
        errors,_=evaluate_case(t,LEDGER)
        self.assertTrue(any('unknown source' in e for e in errors))
    def test_no_receipt_no_execution(self):
        t=copy.deepcopy(CASE)
        t['action']['status']='executed'
        errors,_=evaluate_case(t,LEDGER)
        self.assertIn('execution asserted without tool/action receipt',errors)
    def test_stop_condition_required(self):
        t=copy.deepcopy(CASE)
        t['stop_condition']=''
        errors,_=evaluate_case(t,LEDGER)
        self.assertIn('must state falsifiable stop condition',errors)
    def test_actionable_requires_valid_frozen_forecast(self):
        t=copy.deepcopy(CASE)
        t['decision_mode']='actionable'
        t['forecast_id']='DEMO-ETSY-01'
        errors,_=evaluate_case(t,LEDGER)
        self.assertTrue(any('requires one frozen forecast' in x for x in errors))
        draft=json.loads((ROOT/'templates/forecast_example.json').read_text(encoding='utf-8'))
        errors,_=evaluate_case(t,LEDGER,draft)
        self.assertTrue(any('must be frozen' in x for x in errors))
        draft['forecasts'][0]['opportunity_id']=t['case_id']
        draft['forecasts'][0]=freeze(draft['forecasts'][0])
        errors,_=evaluate_case(t,LEDGER,draft)
        self.assertEqual(errors,[])
    def test_hypothesis_not_proof_of_revenue(self):
        t=copy.deepcopy(CASE)
        t['observations']=[{'kind':'offer_hypothesis','statement':'I can sell','source_ids':[]}]
        _,summary=evaluate_case(t,LEDGER)
        self.assertEqual(summary['stage'],'EARLY_EVIDENCE_ONLY')

if __name__=='__main__':unittest.main()
