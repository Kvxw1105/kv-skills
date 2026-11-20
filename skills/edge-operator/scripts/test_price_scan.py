#!/usr/bin/env python3
import copy
import json
import unittest
from pathlib import Path
from price_scan import normalize
ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((ROOT/'templates/price_scan_example.json').read_text())
class PriceScanTests(unittest.TestCase):
    def test_asks_not_profit(self):
        r=normalize(DATA)
        self.assertEqual(r['asking_price_dispersion_per_unit'],38)
        self.assertFalse(r['execution_ready'])
        self.assertFalse(r['indicative_trade_preconditions_met'])
        self.assertIsNone(r['best_buyer_bid_per_unit'] if 'best_buyer_bid_per_unit' in r else r['best_buyer_bid_net_proceeds_per_unit'])
        self.assertEqual(r['classification'],'asking_price_difference_not_realized_profit')
    def test_bid_is_net_proceeds_not_buyer_total(self):
        x=copy.deepcopy(DATA)
        x['quotes'].append({**x['quotes'][0], 'market':'SAMPLE-PLATFORM-C','listing_ref':'DEMO:bid',
                            'kind':'bid','price':70,'shipping':5,'tax':2,'platform_fee':3,
                            'payment_fee':2,'refund_allowance':1,'buyer_commitment_receipt':None})
        r=normalize(x)
        self.assertEqual(r['best_buyer_bid_net_proceeds_per_unit'],57)
        self.assertEqual(r['buyer_bid_minus_ask_before_unmodeled_costs'],-2)
        self.assertFalse(r['execution_ready'])
        self.assertFalse(r['indicative_trade_preconditions_met'])
    def test_noncomparable_conditions_rejected(self):
        x=copy.deepcopy(DATA);x['quotes'][1]['condition']='used'
        with self.assertRaisesRegex(ValueError,'condition/unit mismatch'):
            normalize(x)
    def test_stale_quotes_rejected(self):
        x=copy.deepcopy(DATA);x['quotes'][1]['observed_at']='2026-11-10T00:00:00+00:00'
        with self.assertRaisesRegex(ValueError,'72h'):
            normalize(x)
    def test_completed_sale_requires_receipt(self):
        x=copy.deepcopy(DATA);x['quotes'][1]['kind']='completed_sale'
        with self.assertRaisesRegex(ValueError,'receipt'):
            normalize(x)
if __name__=='__main__':unittest.main()
