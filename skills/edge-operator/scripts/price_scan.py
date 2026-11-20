#!/usr/bin/env python3
"""Normalize documented cross-market quotes. Never assert actual arbitrage from asks."""
import argparse
import json
from datetime import datetime
from pathlib import Path


def total_cost(q):
    keys=('price','shipping','tax','platform_fee','payment_fee','refund_allowance','fx_to_base')
    for k in keys:
        if type(q.get(k)) not in (int,float) or q[k]<0:
            raise ValueError('invalid/missing nonnegative '+k)
    if q['fx_to_base']<=0:
        raise ValueError('fx_to_base must be positive')
    if type(q.get('quantity')) is not int or q['quantity']<=0:
        raise ValueError('quantity must be positive integer')
    if q['kind']=='bid':
        # Buyer commitment is revenue; delivery/platform/refund reserves reduce seller proceeds.
        amount=q['price']-sum(q[k] for k in ('shipping','tax','platform_fee','payment_fee','refund_allowance'))
    else:
        # Asking price is a buyer's cost, not proven resale proceeds.
        amount=sum(q[k] for k in keys[:6])
    return round(amount*q['fx_to_base']/q['quantity'],4)


def normalize(data):
    quotes=data['quotes']
    if not isinstance(quotes,list) or len(quotes)<2:
        raise ValueError('at least two quotes required')
    if not data.get('base_currency') or not data.get('comparison_key'):
        raise ValueError('missing base_currency/comparison_key')
    result=[]
    seen=set()
    for q in quotes:
        if q.get('kind') not in ('ask','bid','completed_sale'):
            raise ValueError('quote kind ask/bid/completed_sale required')
        for k in ('market','listing_ref','observed_at','condition','region','comparison_key','unit'):
            if not q.get(k):
                raise ValueError('quote missing '+k)
        if not q.get('quote_currency') or not q.get('fx_rate_source'):
            raise ValueError('each quote requires quote_currency and fx_rate_source')
        if q['comparison_key']!=data['comparison_key']:
            raise ValueError('different comparison keys cannot be treated as same asset')
        if not str(q['listing_ref']).startswith('https://') and not str(q['listing_ref']).startswith('DEMO:'):
            raise ValueError('listing_ref must be https URL or explicitly DEMO')
        if q['kind']=='completed_sale' and not q.get('sale_receipt'):
            raise ValueError('completed_sale requires receipt')
        if q['listing_ref'] in seen:
            raise ValueError('duplicate listing_ref')
        seen.add(q['listing_ref'])
        observed=datetime.fromisoformat(q['observed_at'].replace('Z','+00:00'))
        if observed.tzinfo is None:
            raise ValueError('quote timestamp requires timezone')
        result.append({**q,'all_in_base_per_unit':total_cost(q),'parsed_at':observed})
    if len(set(q['condition'] for q in result))>1 or len(set(q['unit'] for q in result))>1:
        raise ValueError('condition/unit mismatch; no like-for-like comparison')
    hours=(max(q['parsed_at'] for q in result)-min(q['parsed_at'] for q in result)).total_seconds()/3600
    if hours>72:
        raise ValueError('quote ages span >72h; not comparable without new scan')
    ask=[q for q in result if q['kind']=='ask']
    bid=[q for q in result if q['kind']=='bid']
    if not ask:
        raise ValueError('no supplier asking quotes')
    cheapest=min(ask,key=lambda q:q['all_in_base_per_unit'])
    pricier=max(ask,key=lambda q:q['all_in_base_per_unit'])
    bestbid=max(bid,key=lambda q:q['all_in_base_per_unit']) if bid else None
    potential=round(bestbid['all_in_base_per_unit']-cheapest['all_in_base_per_unit'],4) if bestbid else None
    executable=bool(bestbid and potential>0 and cheapest.get('authorized_transfer') and
                    cheapest.get('permission_receipt') and cheapest.get('inventory_verified') and
                    cheapest.get('inventory_receipt') and bestbid.get('buyer_commitment_receipt'))
    return {
        'comparison_key':data['comparison_key'], 'base_currency':data['base_currency'],
        'quotes_n':len(result), 'as_of_span_hours':round(hours,2),
        'cheapest_supplier_asking_per_unit':cheapest['all_in_base_per_unit'],
        'highest_supplier_asking_per_unit':pricier['all_in_base_per_unit'],
        'asking_price_dispersion_per_unit':round(pricier['all_in_base_per_unit']-cheapest['all_in_base_per_unit'],4),
        'best_buyer_bid_net_proceeds_per_unit':bestbid['all_in_base_per_unit'] if bestbid else None,
        'buyer_bid_minus_ask_before_unmodeled_costs':potential,
        'indicative_trade_preconditions_met':executable,
        'execution_ready':False, # no transaction may be authorized/executed by a quote-scanning script
        'classification':'indicative_bid_ask_not_a_guaranteed_trade' if bestbid else 'asking_price_difference_not_realized_profit',
        'warning':'indicative preconditions are not authorization to trade. Reverify availability, authenticity, tax, market rules, FX, buyer settlement and unmodeled costs; script never executes trades.'
    }


def main():
    p=argparse.ArgumentParser();p.add_argument('file',type=Path);args=p.parse_args()
    print(json.dumps(normalize(json.loads(args.file.read_text(encoding='utf-8'))),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
