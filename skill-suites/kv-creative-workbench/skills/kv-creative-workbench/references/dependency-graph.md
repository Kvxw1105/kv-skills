# Dependency graph and selective reruns

## Change matrix

| Changed field | Preserve | Mark stale |
|---|---|---|
| root goal | history and raw evidence | framing, candidates, convergence, business, decision |
| commercial_required | framing and mechanisms | business fields, success criteria, decision ranking |
| target user | mechanism and broad problem | scenarios, fit, convergence ranking, payer, channel, validation |
| payer | user need and mechanism | price, channel, sales motion, experiment |
| constraints or resources | framing and problem | feasibility, product form, MVP, test design |
| risk boundary | safe mechanisms and evidence | tactics, channels, product forms, risk assessment |
| candidate mechanism | lineage and raw evidence | convergence, business, decision |
| product form | user need and mechanism | feasibility, channel, MVP, experiment |
| acquisition path | demand and product core | economics, onboarding, experiment |
| new external evidence | unaffected fields | any conclusion contradicted or materially changed by evidence |

## Selective rerun algorithm

1. Increment `case_version`.
2. Record the changed field and reason.
3. Use the matrix to mark dependent fields stale.
4. Preserve stable candidate IDs and lineage.
5. Route to the earliest owner of a stale decisive field.
6. Rerun downstream stages only after the repaired field passes its gate.

Never erase rejected candidates without retaining the rejection reason. They prevent rediscovering the same weak direction later.
