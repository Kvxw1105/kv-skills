# Composition contract

Protocol: `IdeaCase v1.0`.

## Read

- intent.root_goal
- intent.commercial_required
- intent.creativity_level
- context.target_user
- context.user_resources
- context.constraints
- context.risk_boundary
- context.existing_assets
- framing.original_expression
- routing.return_signals
- routing.stale_fields

## Write

- framing.hidden_frames
- framing.loosened_terms
- framing.reframed_questions
- framing.selected_frame_ids
- candidates
- routing.next_stage
- routing.return_signals

## Preserve

Do not overwrite evidence, constraints, existing candidate history, rejection reasons, or downstream fields that are not marked stale.

## Candidate lineage

Use `I-01`, `I-02`, and so on for new candidates. When reframing an existing candidate, create a child ID such as `I-03A` and record `parent_id: I-03`.

## Clean handoff

Do not pass self-praise or final rankings to convergence. Pass mechanism, user, scenario, value, assumptions, dependencies, and source frame.
