# External review response and technical choices (2026-11-20)

This is a response to a *partial* external reading of README, SKILL.md, 96 legacy atoms and 16 RX atoms. The reviewer did not inspect the playbook, mixer, evaluation and scripts in full. This patch explicitly inspected these files before choosing changes.

## 1. Missing calibration loop: ACCEPT, with a stronger settlement contract

The original repo distinguished price quotations, inquiries, deposits and receipts, but could not retrospectively say whether its opportunity predictions were accurate. New files: `calibration-loop.md`, `scripts/calibration.py`, `templates/forecast_example.json` and the opportunity-card overlay. A numerical probability must be attached to a clear cohort, binary event, falsifier and date, then frozen before outcome knowledge. The monthly report computes Brier accuracy, always retaining unresolved and VOID cases. Baseline comparisons use the **same resolved cases**, or remain unavailable.

**Correction to original proposal**: Brier scores cannot automatically separate luck from skill, especially in small or selected samples; nor does a forecast's accuracy tell us which atom caused the outcome. Code does not claim either.

## 2. Inconsistent atom formats: ACCEPT with non-destructive sidecar

Rather than retroactively inventing trigger, evidence and falsifier for 96 prose heuristics, preserve their original text and register each under tier `heuristic`. The 16 RX records are `research_linked`; independent field effectiveness is **still untested**. Registry `atom-registry.json` carries the status, sources and lifecycle. `atom-lifecycle.md` and `scripts/atom_review.py` provide the explore, patch, split and retire review pathway. No automatic deletion or retrospective efficacy inflation.

## 3. Reference classes and competing hypotheses: ACCEPT, WITH EVIDENCE CAVEAT

Add an orientation card with numerical base-rate cohort and provenance or explicit UNKNOWN, prior to the singular case narrative. At least two rival explanations and their disconfirming tests are included. Reference-class training has published evidence in geopolitical forecasting. ACH itself has mixed and at times negative randomized evidence; it is used as **ACH-lite for traceability**, not claimed to improve judgment by itself.

## 4. Position and decay, plus cross-platform scan: ACCEPT

Identify who owns the actual bottleneck and who could bypass the agent's commercial position. Every time-sensitive opportunity records an erosion trigger and a recheck date, but does not fabricate an exact half-life. Cross-market scanner normalizes unit, condition, shipping, fee, tax, source and FX. It does **not** convert two asks into a fictitious trade or issue buy/sell instructions. New cross-market playbook and sandbox synthetic example.

## 5. Cognitive roles are not Agent topology: ACCEPT

Add a front-loaded statement to the archetype mixer that all combinations are **in-agent cognitive lenses** by default. Deploying separate worker Agents is justified only by different tools, independent tasks and measured net coordination benefit. MAST provides relevant observed failure modes, not a theorem that multiple Agents always fail.

## 6. System metrics and owner awareness: ACCEPT with denominator discipline

Track falsification latency, independently adjudicated gate false blocks and annotated luck context. Missing data stays missing; subjective luck annotation is **not** a computed causal fraction of profits. Preserve compact human input at direction and settlement, without repeatedly gating already authorized reversible work. The user acts as external calibration, not a daily data-entry clerk.

## Structural and scientific limitations

- This patch introduces deterministic code and tests. It does not provide verified customer payments, live trade scans, long-horizon user outcomes or controlled cross-model behavioral comparisons.
- The proposal's named 'Bayesian-Agent explore/patch/split/retire' cannot be imported as an empirically verified canonical algorithm without exact source and implementation. The lifecycle states here are defined locally; Beta(1,1) posterior on *discordant held-out controlled pairs* is explicitly only a descriptive candidate-screening device.
- The other team's pilot-A settlement schema was not supplied. `interoperability.md` defines a portable Edge Operator contract but does not assert tested compatibility with a missing external schema.
- A local SHA fingerprint guards a frozen record against accidental changes; it is not a trusted independent timestamp. Commit it before resolution for stronger provenance.
- Brier score, user value, fraud/safety, profits and lifecycle decisions are distinct measurement axes.

## Primary sources

GJP: https://escholarship.org/uc/item/4rg4n9vr
ACH randomized counterevidence: https://onlinelibrary.wiley.com/doi/full/10.1002/acp.3550
ACH probability-coherence follow-up: https://www.cambridge.org/core/journals/judgment-and-decision-making/article/coherence-of-probability-judgments-from-uncertain-evidence-does-ach-help/9ED40E4658EE77914D2C7A265154B59A
MAST: https://arxiv.org/abs/2503.13657
Brier sampling uncertainty: https://doi.org/10.1175/2007WAF2007049.1
