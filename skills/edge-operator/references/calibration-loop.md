# Calibration loop: commit, act, settle, learn (v1.2)

**Goal**: An agent must be accountable for judgments, not only the evidence it collected. Forecast scores measure predictive accuracy; actual profits, customer welfare and authorized execution are separate endpoints. Never equate them.

## Scope and friction budget

Run the full protocol when the agent selects, rejects, budgets, publicly asserts, or repeatedly operates on a commercial opportunity. A single exploratory brainstorm, ordinary creative work or a low-impact lookup may skip the full card. Never invent a probability to satisfy a template: leave the record in DRAFT until an event can be defined honestly. Keep the final user-facing message short.

## 0. Direction card before conviction

Use `templates/orientation_card.md`. First define the reference class **before** the persuasive story about this opportunity. Record selection criteria, data collection dates, denominator, events, rate, and source. If no suitable comparison cohort exists, set the baseline explicitly to UNKNOWN: do not substitute a made-up 50% rate. Then write at least 2 competing hypotheses, with the most discriminating **disconfirming** evidence for each. ACH-style matrices are a forcing function, not a guaranteed accuracy booster; controlled studies found mixed or negative benefits. Use probabilities and coherent updating separately.

Also map who captures value, whose permission matters, what could bypass our position, and what would erase the edge. If you do not control entry, price or settlement, identify which party does before calling an information gap a business advantage. Every window gets an erosion trigger and recheck date. `recheck_on` is an attention reminder, not an estimated physical half-life.

## 1. Define a resolvable prediction

For an actionable idea, include these non-negotiable fields in the opportunity card:

- **Numeric probability** `p` in [0,1] for an explicit *binary event*, with cohort, start, threshold and exclusion conditions. Mark it an analyst estimate, not a fact.
- **Disproof metric**: a measurable observation capable of falsifying the claim, including what counts as a counterexample.
- **Settlement deadline** `settle_by` as an ISO calendar date, a reliable evidence path, and a named resolver.

Record evidence tier, competing explanations and base-rate data separately. Price-offer observations, customer interviews, deposits, net receipts and refunds cannot substitute for one another. Prefer events such as `at least one paid deposit among 10 eligible, consenting contacted sellers by date D` over vague `this market has potential`. If the predeclared trial/cohort cannot be completed, mark the forecast VOID with a reason and receipt, not an artificial loss.

## 2. Freeze before acting

Edit `templates/forecast_example.json` into a new local forecast book. The bundled example is **DRAFT and fictitious**.

```
python scripts/calibration.py validate path/to/forecasts.json
python scripts/calibration.py freeze path/to/forecasts.json OPPORTUNITY_FORECAST_ID
```

Freeze records UTC time and SHA-256 of the locked forecast fields. Subsequent changes to probability, outcome definition, reference class, hypotheses, atom IDs, settlement date, strategic position or decay invalidate the fingerprint. **Local time and hashes are not independent trusted timestamps.** Commit a forecast to a remote repository or signed, append-only journal before the relevant result is observed if auditability matters. Do not mutate old forecasts to improve the track record: create a new forecast revision with a new ID and a cross-reference.

## 3. Execute with minimal yet real human contact

At the *orientation* checkpoint, show the human a 30-second packet: `claim / base rate / competing explanation / bottleneck owner / expected payoff / proposed authorized action / what would disprove us`. This is not a request for repeated micro-approvals. Ordinary reversible activity within prior scope can proceed. Account outreach, public posting, access to others' data, spending or irreversible actions still need actual permission.

At *settlement*, present a compact receipt, outcome and what will change in strategy. Preserve the human's ability to detect odd assumptions and confront external reality: do not fully hide the critical inputs, contrary evidence and misses behind a confident recommendation. If human feedback changes the forecast, open a new revision; do not overwrite frozen history.

## 4. Settle or void

```
python scripts/calibration.py settle path/to/forecasts.json ID 1 RECEIPT_REF --adjudicator reviewer
python scripts/calibration.py settle path/to/forecasts.json ID 0 RECEIPT_REF --adjudicator reviewer
python scripts/calibration.py void path/to/forecasts.json ID RECEIPT_REF --reason 'predeclared cohort could not be assembled'
python scripts/calibration.py report path/to/forecasts.json
```

Only events that have genuinely resolved to 0 or 1 may be Brier-scored. A missed deadline with missing evidence remains *overdue/unresolved*, not a scored failure. A VOID record stays visible in the denominator of attempted tests, but is excluded from predictive accuracy. If a third-party receipt is forged, the validator cannot know; independent review is still required.

## 5. Monthly settlement review

For settled forecasts, calculate binary Brier `(p-y)^2` (lower is better, range 0..1) and aggregate over comparable, predeclared questions. Compare Brier against **the same resolved subset's** reference-class forecast when a genuine cohort baseline exists. The `Brier skill` helper reports `1 - Brier_model/Brier_baseline`; it is omitted when the baseline is absent or zero. If the number of observations is small, output descriptive statistics only, no improvement claim. Even a properly scored series may have luck, correlated episodes, sample selection or question-design bias.

After settlement, audit which assumptions failed. Do not attribute a business win to each of 5–12 invoked thinking atoms. A randomized paired or pre-registered ablation that changes one atom/step is stronger than an anecdotal success. See `atom-lifecycle.md`.

## 6. Process metrics, not theater

Compute with `python scripts/ops_metrics.py templates/ops_metrics_example.json`:

- **Falsification latency**: time between a recorded disconfirming observation and the documented strategy correction, with open incidents retained separately.
- **False block rate**: among independently reviewed *valid* proposed actions, share incorrectly blocked. Report the adjudicated sample and selection bias; a sample of convenient reviews is not the true universal FPR.
- **Luck attribution annotation coverage**: among completed wins, how many received a structured luck/contributing-context annotation? Unknown is allowed. This is **not** a numerical measurement of what fraction of profit was due to luck.

Keep paired denominators, all absent values, and unresolved cases visible. Monthly review means a *manual schedule expectation*, not an automation that has magically been installed.

## Sources and what they do/do not show

- Mellers et al., `Psychological Strategies for Winning a Geopolitical Forecasting Tournament` (2014): reference-class training, team discussion and tracking improved forecast judgment in that setting. https://escholarship.org/uc/item/4rg4n9vr
- Brier proper scoring and calibration review: https://link.springer.com/article/10.1007/s10994-023-06336-7
- Sampling uncertainty for Brier scores, especially rare events: https://doi.org/10.1175%2F2007WAF2007049.1
- CIA `Tradecraft Primer` ACH description: https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf
- ACH counter-evidence: https://www.cambridge.org/core/journals/judgment-and-decision-making/article/coherence-of-probability-judgments-from-uncertain-evidence-does-ach-help/9ED40E4658EE77914D2C7A265154B59A

A useful checklist is a **hypothesis about better agent behavior** until controlled performance tests establish its incremental value.
