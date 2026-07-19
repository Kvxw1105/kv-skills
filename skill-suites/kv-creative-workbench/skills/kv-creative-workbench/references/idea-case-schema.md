# IdeaCase v1.0

Use one state object across framing, divergence, convergence, validation, and decision. The object is a working protocol, not a mandatory user-facing format.

```yaml
protocol: IdeaCase
protocol_version: "1.0"
case_id: "IC-YYYYMMDD-01"
case_version: 1
stage: intake
mode: standard

intent:
  root_goal: ""
  requested_output: ""
  commercial_required: false
  decision_horizon: ""
  creativity_level: standard
  success_definition: ""

context:
  target_user: ""
  payer: ""
  beneficiary: ""
  user_resources: []
  constraints: []
  risk_boundary: ""
  existing_assets: []
  evidence: []
  assumptions: []

framing:
  original_expression: ""
  hidden_frames: []
  loosened_terms: []
  reframed_questions: []
  selected_frame_ids: []

candidates:
  - id: I-01
    parent_id: null
    status: generated
    name: ""
    mechanism: ""
    target_user: ""
    use_scenario: ""
    value_created: ""
    medium_or_product_form: ""
    novelty_source: ""
    assumptions: []
    dependencies: []
    evidence_level: hypothesis
    preserved_core: []

convergence:
  reviewed_candidate_ids: []
  promoted: []
  transformed: []
  archived: []
  rejected: []
  portfolio_roles: {}
  ranking_basis: []

business:
  candidate_id: ""
  pain_or_job: ""
  urgency: ""
  user: ""
  payer: ""
  beneficiary: ""
  current_substitute: ""
  switching_reason: ""
  willingness_to_pay_hypothesis: ""
  acquisition_path: ""
  product_form: ""
  mvp: ""
  experiment: ""
  success_threshold: ""
  kill_criteria: []
  risks: []
  evidence_gaps: []

routing:
  completed_stages: []
  return_signals: []
  stale_fields: []
  next_stage: ""

decision:
  chosen_candidate_id: ""
  rationale: ""
  accepted_tradeoff: ""
  confidence: ""
  unknowns: []
  next_action: ""
```

## Field rules

- Keep IDs stable across all stages.
- Increment `case_version` whenever a decisive assumption changes.
- Mark changed and dependent fields in `routing.stale_fields` before rerunning.
- Separate user, payer, and beneficiary whenever they may differ.
- Store unsupported market statements as hypotheses or evidence gaps.
- Do not require every field for lightweight routes. Populate only what the selected route needs.
