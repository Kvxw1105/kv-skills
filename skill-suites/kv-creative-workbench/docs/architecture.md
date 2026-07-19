# Architecture

## Control plane and specialists

`kv-creative-workbench` is the control plane. It owns intake, state, routing, selective invalidation, stopping conditions, and the final decision. The other three skills are specialists with narrow ownership boundaries.

- `kv-language-ideation` owns framing and divergence.
- `kv-idea-convergence` owns independent review, creative-core extraction, transformation, and narrowing.
- `kv-business-opportunity-strategist` owns commercial actor logic, demand, distribution, MVP experiments, and kill criteria.

The controller may invoke one specialist, several specialists, or a compact fallback. A specialist is counted as activated only after its instructions are loaded and applied.

## Shared state

The suite uses `IdeaCase v1.0` as the shared case record. Stable candidate IDs and lineage are preserved across reruns. Evidence, assumptions, rejected candidates, and return signals remain traceable rather than being overwritten.

## Selective invalidation

When an upstream field changes, only dependent fields become stale. For example, changing the payer preserves the problem and mechanism while invalidating pricing, channel, sales motion, and the commercial experiment. This prevents a small correction from restarting the entire workflow.

## Runtime boundary

Host platforms differ in automatic Skill discovery and cross-Skill invocation. The suite documents semantic composition, but does not claim a platform-level broadcast or sub-agent API. When a specialist cannot be loaded, the controller uses its bundled compact fallback and discloses the reduced depth when material.
