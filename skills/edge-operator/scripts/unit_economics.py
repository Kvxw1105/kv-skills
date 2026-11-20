#!/usr/bin/env python3
"""Scenario-based order economics. Not a market forecast or proof of actual sales."""
import argparse
import json
import math
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = (
    "price", "refund_rate", "refund_handling_cost", "fulfillment_cost",
    "api_cost", "labor_cost", "customer_acquisition_cost", "payment_fee_percent",
    "payment_fee_fixed", "monthly_fixed_cost", "expected_orders_per_month",
)


def dec(value, key):
    try:
        if isinstance(value, bool):
            raise ValueError(key)
        v = Decimal(str(value))
        if not v.is_finite():
            raise ValueError(key)
        return v
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"{key}: expected a finite number")


def calculate(obj):
    missing = [key for key in REQUIRED if key not in obj]
    if missing:
        raise ValueError("Missing keys: " + ", ".join(missing))
    values = {key: dec(obj[key], key) for key in REQUIRED}
    if any(value < 0 for value in values.values()):
        raise ValueError("Costs, rates, and counts must be nonnegative")
    if values["price"] <= 0:
        raise ValueError("price must be > 0")
    if values["refund_rate"] > 1 or values["payment_fee_percent"] > 1:
        raise ValueError("Percentage fields must be fractions in [0,1]")
    if values["expected_orders_per_month"] != values["expected_orders_per_month"].to_integral_value():
        raise ValueError("expected_orders_per_month must be an integer")

    a = values
    gross = a["price"]
    expected_rev = gross * (Decimal(1) - a["refund_rate"])
    # Conservative: assume payment processing fee is incurred for all orders and is not refunded.
    processing = gross * a["payment_fee_percent"] + a["payment_fee_fixed"]
    variable = a["fulfillment_cost"] + a["api_cost"] + a["labor_cost"] + a["customer_acquisition_cost"]
    expected_refund_cost = a["refund_handling_cost"] * a["refund_rate"]
    contribution = expected_rev - processing - variable - expected_refund_cost
    monthly_contribution = contribution * a["expected_orders_per_month"] - a["monthly_fixed_cost"]
    breakeven = None
    if contribution > 0:
        breakeven = int((a["monthly_fixed_cost"] / contribution).to_integral_value(rounding="ROUND_CEILING"))

    def round2(v):
        return float(v.quantize(Decimal("0.01")))

    return {
        "scenario_name": obj.get("scenario_name", "scenario"),
        "currency": obj.get("currency", "units"),
        "data_quality": obj.get("data_quality", "unknown; confirm all inputs"),
        "expected_recognized_revenue_per_order": round2(expected_rev),
        "expected_payment_fee_per_order": round2(processing),
        "expected_variable_cost_per_order": round2(variable),
        "expected_refund_handling_per_order": round2(expected_refund_cost),
        "expected_contribution_per_order": round2(contribution),
        "expected_contribution_after_fixed_per_month": round2(monthly_contribution),
        "break_even_orders_per_month": breakeven,
        "assumptions": "Refunds reverse full revenue but all variable costs and processing fees still occur. Costs are inputs, not observed facts; excludes taxes and working capital."
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("scenario_json", type=Path)
    p.add_argument("--json", action="store_true", help="output JSON for other agents")
    args = p.parse_args()
    result = calculate(json.loads(args.scenario_json.read_text(encoding="utf-8")))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
