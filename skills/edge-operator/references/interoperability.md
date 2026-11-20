# Portable calibration exchange contract

## Purpose

Use a stable field contract when copying forecasts across cloud, desktop and phone Agents. **This is an Edge Operator v1.2 contract, not proof of compatibility with the other AI team's already-existing pilot A format.** A verified explicit field map is needed before claiming lossless migration.

**Canonical record**: `templates/forecast_example.json` includes `forecasts[]` of:

| Semantic field | Canonical key | Meaning |
| --- | --- | --- |
| Unique prediction | `forecast_id` | Revisions must use new IDs |
| Commercial case | `opportunity_id` | Links to money/evidence case |
| Binary event | `outcome_definition` | What exact cohort, threshold, date and failure count as 0/1 |
| Subjective probability | `probability` | Numeric p from 0 to 1; not a base rate |
| Falsifying observation | `falsifier` | Measurable counterexample |
| Settlement date | `settle_by` | Calendar deadline, YYYY-MM-DD |
| Comparable cohort | `reference_class` | `sample_n`,`success_n`,`base_rate`,`source_ref`,`as_of`,`selection_bias` or all unknown |
| Rival mechanisms | `hypotheses[]` | At least 2 with disconfirming tests; not probabilistic ACH certainty |
| Value capture | `position` | Bottleneck owner, bypass, own position, value to capture |
| Edge erosion | `decay` | Why gap remains, what erases it, recheck date |
| Cognitive lenses | `atom_ids[]` | IDs from `atom-registry.json`; no causal credit inferred |
| Locked commitment | `frozen_at`,`forecast_sha256` | Local integrity, not trusted timestamp |
| Resolution | `state`,`outcome` | DRAFT/FROZEN/SETTLED/VOID; resolved numeric outcome plus evidence and reviewer |

## Import/export minimum

Keep UTF-8 JSON with ISO 8601 timezone-aware timestamps. Export in a single `forecasts[]` book, preserving original `forecast_id`, `frozen_at`, hash, and the exact locked fields. Do not modify source timestamps or secretly rescale probabilities from 0..1 to 0..100. If an external model uses percent, divide by 100 and log the conversion. Keep separate identities for claim author, reviewer and execution Agent. Treat unreviewed imports as unverified.

For another team's settlement schema, use explicit field mapping, record type transforms and a migration test that proves no loss of frozen history, void reasons, baseline denominators or receipt links. Until provided, exchange via this JSON document and mark mapping status `unverified`.

## User oversight and agent coordination

The orchestrator may route research, coding and data collection across workers, but only one canonical settlement ledger should own a forecast ID. For competing team forecasts, record both under separate IDs before sharing one resolved event ID and outcome. Individual agents must not score their own forecasts after learning the outcome. The user receives a brief direction packet and settlement packet with disagreement and receipt; their role is quality calibration, not manual micromanagement.
