# Atom registry and lifecycle: explore / patch / split / retire (v1.2)

## Two evidence tiers, not a flat '112 proven skills'

The original 96 prose atoms are marked `heuristic`. All 16 RX atoms are marked `research_linked`: their external citations are traceable, but their *incremental impact on agent outputs or net business income has not been established*. Both start with lifecycle `candidate`, observed trial count **zero**. A source about a mechanism is not a field validation of the prompt. The sidecar `atom-registry.json` records evidence and lifecycle without rewriting or fabricating the original texts.

The 112 entries are not 112 autonomous workers. Choose only a few cognitive lenses relevant to a task. Separate an invocation plan from an independent worker deployment, which requires a cost/benefit case. See MAST (NeurIPS 2025): https://arxiv.org/abs/2503.13657

## Lifecycle states and allowed transitions

| State | Meaning | How to enter | How to leave |
| --- | --- | --- | --- |
| `candidate` | Untested or only sourced | Initial registry/import | Evidence-plan review -> `trial` |
| `trial` | Predeclared test active | Eligible task cohort, baseline, criterion, receipts | Review outcomes -> `promoted`, `patched`, `split`, or `retired` |
| `promoted` | Repeatably useful *within a named scope* | Independent held-out comparisons, predeclared criteria, human check | Context shift or regression -> `patched`/`retired` |
| `patched` | Revised formulation, same hypothesis family | Logged diagnosis, changed prompt text, new version | Must retrial; old results retain version ID |
| `split` | Different outcomes across contexts require separate rules | Named contexts + traceable forks | Validate each child atom, retire broad original if needed |
| `retired` | Poor evidence or obsolete | Logged review, replacement or honest negative evidence | Re-entry as a **new version** with fresh evaluation |

Do not delete retirement history. A retirement candidate is a **human-review recommendation**, not an automatic deletion. Never imply repeated observed sales prove one particular atom caused them.

## Paired evidence and optional posterior

Use `templates/atom_trials_example.json` and `scripts/atom_review.py` when independent controlled runs are actually available. For a trial, record `atom_id`, task ID, context ID, treatment/control success, two independent receipts, evaluator, randomized-paired vs observational design and whether the task was held out.

The optional Beta(1,1) update uses *discordant held-out paired outcomes only*:

- A `win` means **treatment succeeded, control failed** on the same task.
- A `loss` means **control succeeded, treatment failed**.
- Both success and both failure are *ties*, not evidence that one atom is superior.
- The posterior estimates `P(win among discordant outcomes)`; it does NOT estimate sale probability, real-world causal effect or forecast calibration.

Before even suggesting promotion or retirement, this conservative implementation requires at least 20 reviewed held-out controlled pairs, 5 different contexts and 10 informative discordant pairs, plus posterior probability >0.95 or <0.05 respectively. **These are local process thresholds chosen for restraint, not established scientific guarantees.** Actual decisions require reading task quality, independent confidence checks, drift, costs and downstream behavior. Nonrandomized observations do not change the posterior.

If several atoms changed simultaneously, label the run `uncontrolled_observation`. Do not award individual credit to all of them. Separate what the model *said* from executed tool outputs and paid customer outcomes. If a historical cohort is not available, keep a baseline unknown; do not invent synthetic successes.

## Review questions

1. In what exact context was the atom triggered, and what observable action did it change?
2. What is the best competing explanation or confounder (source freshness, skill overlap, better tools, evaluator leakage, luck)?
3. Did it beat the baseline on a metric the user actually values (accuracy, net cash, time, successful authorized action, proof quality)?
4. Which task contexts failed? If behavior differs, *split* instead of optimizing a general slogan.
5. Which patch changes the smallest causal mechanism? Log patch version, re-test on fresh held-out tasks.
6. Is the actor roster increasing coordination overhead? Single-agent internal lenses are the default.

## Required review output

`atom_id | version | tier | lifecycle | trials_n | heldout_n | baseline_delta | failure contexts | decision | reviewer | next_review_on | archived_evidence_refs`.

No tests means `not measured`, not `0% win rate`. Retirement candidates remain in the registry with references and a clear reason, but are excluded from default prompt selection. No automatic monthly task is created by these documents or scripts.
