# Actor and payer map

## Roles

- User: operates or directly experiences the offer.
- Beneficiary: receives the outcome.
- Payer: controls the budget.
- Buyer or approver: authorizes adoption.
- Influencer: shapes trust or selection.
- Blocker: can prevent use through policy, workflow, or incentives.

## Mapping questions

- Who feels the pain at the triggering moment?
- Who has authority to change the workflow?
- Who bears the cost of the current state?
- Who owns the relevant budget?
- Who faces risk if the product fails?
- Who must trust the result?

## Common patterns

### Consumer

User, beneficiary, payer, and buyer are often the same person.

### Parent and child

Child is user and beneficiary; parent is payer and buyer; school or teacher may influence or block.

### Employee and employer

Employee is user; manager or company is payer; compliance, IT, or procurement may approve or block.

### Professional service

Professional is user; client is beneficiary and payer; firm leadership may buy.

### Platform ecosystem

Creator or merchant is user; audience may benefit; platform controls access and can block.

Incorrect actor mapping often creates false pricing and channel conclusions. Return `SPLIT_USER_PAYER` when needed.
