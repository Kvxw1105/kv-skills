#!/usr/bin/env python3
"""Deterministic smoke tests; these do not test an LLM's quality or external execution."""
import unittest
from decimal import Decimal
from unit_economics import calculate
from validate_mission import validate


class FinanceTests(unittest.TestCase):
    def setUp(self):
        self.scenario = {
            "price": 300, "refund_rate": 0.1, "refund_handling_cost": 5,
            "fulfillment_cost": 80, "api_cost": 20, "labor_cost": 10,
            "customer_acquisition_cost": 30, "payment_fee_percent": 0.03,
            "payment_fee_fixed": 1, "monthly_fixed_cost": 600,
            "expected_orders_per_month": 10,
        }

    def test_example(self):
        r = calculate(self.scenario)
        self.assertEqual(r["expected_recognized_revenue_per_order"], 270)
        self.assertEqual(r["expected_payment_fee_per_order"], 10)
        self.assertEqual(r["expected_variable_cost_per_order"], 140)
        self.assertEqual(r["expected_refund_handling_per_order"], 0.5)
        self.assertEqual(r["expected_contribution_per_order"], 119.5)
        self.assertEqual(r["expected_contribution_after_fixed_per_month"], 595)
        self.assertEqual(r["break_even_orders_per_month"], 6)

    def test_reject_invalid_probability(self):
        self.scenario["refund_rate"] = 1.4
        with self.assertRaises(ValueError):
            calculate(self.scenario)

    def test_unprofitable_has_no_break_even(self):
        self.scenario["price"] = 20
        self.assertIsNone(calculate(self.scenario)["break_even_orders_per_month"])


class MissionTests(unittest.TestCase):
    def test_minimal_valid(self):
        data = {"mission_id": "t1", "goal": "a", "true_success": "b", "mode": "x", "authority": {}, "tasks": [{
            "task_id": "t1-1", "owner_role": "research", "goal": "find", "status": "PROPOSED", "evidence_to_return": "URL"
        }]}
        self.assertEqual(validate(data), [])

    def test_blocks_ungranted_external_action(self):
        data = {"mission_id": "t1", "goal": "a", "true_success": "b", "mode": "x", "authority": {}, "tasks": [{
            "task_id": "t1-1", "owner_role": "publish", "goal": "post", "status": "PROPOSED",
            "evidence_to_return": "URL", "requires_external_action": True,
        }]}
        self.assertTrue(any("external action" in e for e in validate(data)))


if __name__ == "__main__":
    unittest.main()
