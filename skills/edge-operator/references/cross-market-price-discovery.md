# Cross-market price discovery: inspect differences, verify capture

Scan observable marketplace or service quotes, across languages and geographies where legitimate. A displayed difference is often explained by noncomparable goods, taxes, delivery time, account restrictions, warranties, counterfeit risks or simply the absence of a real buyer bid.

## Minimum data contract

- Precisely define the comparable good/result: canonical SKU, licensing, grade, condition, unit, bundle size, scope, geography, access and refund terms.
- Record source URL, platform, observed timestamp in timezone, bid/ask/completed sale status, quote currency, quote quantity and FX conversion to a stated base currency.
- Record buyer expenses separately from seller net proceeds: fees, transport, tax, refund reserve, payment fees, exchange/withdrawal and return exposure. Don't call a seller's asking price an executable buy order.
- Recheck quotes within 72h for fast-moving opportunities. That is an internal freshness guard, not a law of markets; refresh sooner if volatility is high.
- Determine value capture and bypass: who holds stock, merchant permissions, buyer reach, settlement, guarantee and the bottleneck. If the source and buyer can transact directly without you, specify the tangible reason to involve you.
- Look for decay: platform repricing, currency moves, supply changes, new entrants, promotions, policy enforcement and direct matching.

## Use

Run `python scripts/price_scan.py templates/price_scan_example.json`. Sample prices are entirely synthetic. The program normalizes quotes and computes **asking-price dispersion**, not realized arbitrage. It can report indicative buyer-bid minus buyer-ask if actual buyer quotes are supplied, while explicitly avoiding claims of a closed trade.

If quote definition, condition or unit differ, fail comparison. If the exact bid, inventory, authorization or payment is unknown, leave `execution_ready=false`. If a quote expires, record how and when it was rechecked. No scraping outside permissions, no abuse of coupons or access controls, no unauthorised transfers. Prefer a proven service gap to a dubious commodity resale spread.

## Evidence progression

`Ask listings -> matching verified quotes -> inventory and terms -> genuine buyer bid -> authorized test transaction -> fee reconciliation -> net received -> repeatable availability`.

Do not substitute a hypothetical platform flip for proof of an executed trade. Use this as a separate playbook only when users explicitly want cross-market comparison or when a market's structure makes it relevant. Most ordinary consumer opportunities need not run a continuous scanner.
