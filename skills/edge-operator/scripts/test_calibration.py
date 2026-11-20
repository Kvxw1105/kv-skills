#!/usr/bin/env python3
"""Deterministic calibration contract tests; not real forecasts or customer contact."""
import copy
import json
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from calibration import validate_forecast,validate_book,freeze,settle,void_forecast,report,fingerprint

ROOT=Path(__file__).resolve().parent.parent
EXAMPLE=json.loads((ROOT/'templates/forecast_example.json').read_text(encoding='utf-8'))

class CalibrationTests(unittest.TestCase):
    def setUp(self):
        self.f=copy.deepcopy(EXAMPLE['forecasts'][0])
        self.at=datetime(2026,11,20,11,0,tzinfo=timezone.utc)
    def test_valid_draft_and_no_scored_transaction(self):
        self.assertEqual(validate_forecast(self.f),[])
        r=report({'forecasts':[self.f]},today=date(2026,11,20))
        self.assertIsNone(r['brier_mean'])
        self.assertEqual(r['draft'],1)
    def test_refuses_untrusted_base_rate(self):
        self.f['reference_class']['base_rate']=.5
        self.assertTrue(any('unknown cohort' in e for e in validate_forecast(self.f)))
    def test_mismatched_base_rate(self):
        self.f['reference_class'].update({'sample_n':5,'success_n':1,'base_rate':.5,'source_ref':'https://example.org/observed','as_of':'2026-11-20'})
        self.assertTrue(any('base_rate does not match' in e for e in validate_forecast(self.f)))
    def test_event_needs_disproof_and_settlement(self):
        self.f['falsifier']=''
        self.f['settle_by']='no-date'
        self.assertTrue(any('falsifier' in e for e in validate_forecast(self.f)))
        self.assertTrue(any('settle_by' in e for e in validate_forecast(self.f)))
    def test_competing_hypotheses(self):
        self.f['hypotheses']=self.f['hypotheses'][:1]
        self.assertTrue(any('competing hypotheses' in e for e in validate_forecast(self.f)))
    def test_freeze_fingerprint_blocks_probability_rewrite(self):
        x=freeze(self.f,self.at)
        self.assertEqual(validate_forecast(x),[])
        x['probability']=.99
        self.assertTrue(any('fingerprint mismatch' in e for e in validate_forecast(x)))
    def test_freeze_fingerprint_blocks_bottleneck_rewrite(self):
        x=freeze(self.f,self.at)
        x['position']['bottleneck_owner']='changed after event'
        self.assertTrue(any('fingerprint mismatch' in e for e in validate_forecast(x)))
    def test_settle_receipt_and_brier(self):
        x=freeze(self.f,self.at)
        y=settle(x,0,'test:independent-fictional-receipt','test-evaluator',datetime(2027,1,31,tzinfo=timezone.utc))
        self.assertEqual(validate_forecast(y),[])
        r=report({'forecasts':[y]})
        self.assertAlmostEqual(r['brier_mean'],.0225)
        self.assertIsNone(r['brier_skill_vs_cohort'])
        self.assertEqual(r['settled_missing_baseline'],1)
    def test_cannot_settle_without_receipt(self):
        x=freeze(self.f,self.at)
        with self.assertRaises(ValueError):
            settle(x,1,'',resolved_at=datetime(2026,12,20,tzinfo=timezone.utc))
    def test_late_and_void_handling(self):
        x=freeze(self.f,self.at)
        r=report({'forecasts':[x]},today=date(2027,2,1))
        self.assertEqual(r['overdue_open'],1)
        v=void_forecast(x,'not enough eligible contacts','test:no-outreach-run')
        r=report({'forecasts':[v]},today=date(2027,2,1))
        self.assertEqual(r['void_n'],1)
        self.assertEqual(r['settled_n'],0)
        self.assertIsNone(r['brier_mean'])
    def test_paired_baseline_same_subset(self):
        x=copy.deepcopy(self.f)
        x['reference_class'].update({'sample_n':10,'success_n':3,'base_rate':.3,'source_ref':'test:historical-records','as_of':'2026-11-19'})
        x['probability']=.8
        a=settle(freeze(x,self.at),1,'test:resolved','test-evaluator',datetime(2027,1,31,tzinfo=timezone.utc))
        b=settle(freeze(self.f,self.at),0,'test:resolved','test-evaluator',datetime(2027,1,31,tzinfo=timezone.utc))
        b['forecast_id']='other'
        # changing an ID after freezing must be rejected; create separate frozen forecast instead
        self.assertTrue(any('fingerprint mismatch' in e for e in validate_forecast(b)))
        b=copy.deepcopy(self.f);b['forecast_id']='other'
        b=settle(freeze(b,self.at),0,'test:resolved','test-evaluator',datetime(2027,1,31,tzinfo=timezone.utc))
        r=report({'forecasts':[a,b]})
        self.assertEqual(r['paired_baseline_n'],1)
        self.assertAlmostEqual(r['paired_forecast_brier'],.04)
        self.assertAlmostEqual(r['paired_baseline_brier'],.49)
        self.assertAlmostEqual(r['brier_skill_vs_cohort'],1-.04/.49)
    def test_duplicate_records(self):
        self.assertTrue(any('duplicate forecast ID' in e for e in validate_book({'forecasts':[self.f,self.f]})))
    def test_no_invalid_probability_bool(self):
        self.f['probability']=True
        self.assertTrue(any('numeric probability' in e for e in validate_forecast(self.f)))

if __name__=='__main__':unittest.main()
