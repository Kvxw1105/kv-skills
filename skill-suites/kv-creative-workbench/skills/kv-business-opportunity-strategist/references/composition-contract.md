# Composition contract

Protocol: `IdeaCase v1.0`.

## Read

- intent.root_goal, requested_output, commercial_required, horizon, and success definition;
- context target user, payer, beneficiary, resources, constraints, risk boundary, evidence, and assumptions;
- finalist candidate IDs, lineage, mechanisms, scenarios, values, dependencies, and unresolved risks;
- convergence roles and reasons;
- routing stale fields and return signals.

## Write

- business fields for each evaluated finalist;
- evidence gaps;
- validation experiment and thresholds;
- kill criteria;
- routing return signals;
- readiness for decision.

## Preserve

Do not overwrite candidate mechanisms or convergence history unless returning a transformation signal. Keep facts, user-provided evidence, and hypotheses distinct.

## Handoff

Return a compact commercial packet and one explicit signal. If multiple candidates are evaluated, identify the strongest and the condition under which another candidate would become preferable.
