#!/usr/bin/env python3
import unittest
from ops_metrics import metrics
class MetricsTests(unittest.TestCase):
    def test_empty_unknown_not_zero(self):
        m=metrics({'gate_reviews':[],'falsifications':[],'successful_outcomes':[]})
        self.assertIsNone(m['gate_false_block_rate_on_independently_reviewed_valid_cases'])
        self.assertIsNone(m['luck_marked_contributing_fraction_among_known_annotations'])
    def test_denominators(self):
        x={'gate_reviews':[{'gate_decision':'block','adjudication':'claim_valid'},
                          {'gate_decision':'allow','adjudication':'claim_valid'},
                          {'gate_decision':'block','adjudication':'claim_invalid'},
                          {'gate_decision':'block','adjudication':'unknown'}],
           'falsifications':[{'disproof_detected_on':'2026-11-20','decision_corrected_on':'2026-11-22'},
                             {'disproof_detected_on':'2026-11-20','decision_corrected_on':None}],
           'successful_outcomes':[{'luck_annotation':'contributed'},
                                  {'luck_annotation':'unknown'},
                                  {'luck_annotation':'not_observed'}]}
        r=metrics(x)
        self.assertEqual(r['gate_false_block_rate_on_independently_reviewed_valid_cases'],.5)
        self.assertEqual(r['falsification_delay_days_mean'],2)
        self.assertEqual(r['falsification_delay_unresolved_n'],1)
        self.assertEqual(r['luck_marked_contributing_fraction_among_known_annotations'],.5)
        self.assertEqual(r['luck_annotations_unknown_n'],1)
if __name__=='__main__':unittest.main()
