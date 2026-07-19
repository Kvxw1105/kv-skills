# Composition contract

Protocol: `IdeaCase v1.0`.

## Read

- intent and success definition;
- context resources, constraints, risk boundary, evidence, and assumptions;
- framing selected frames;
- candidate IDs, lineage, mechanisms, scenarios, values, assumptions, dependencies, and evidence levels;
- routing stale fields and return signals.

## Write

- convergence.reviewed_candidate_ids;
- convergence.promoted;
- convergence.transformed;
- convergence.archived;
- convergence.rejected;
- convergence.portfolio_roles;
- convergence.ranking_basis;
- transformed child candidates;
- routing.return_signals and routing.next_stage.

## Preserve

Do not overwrite framing history, raw evidence, or business fields not marked stale. Retain rejected IDs and reasons.

## Handoff rule

Pass no more than three candidates downstream. Remove generator hype and rankings. Include the decisive assumptions that business validation must test.
