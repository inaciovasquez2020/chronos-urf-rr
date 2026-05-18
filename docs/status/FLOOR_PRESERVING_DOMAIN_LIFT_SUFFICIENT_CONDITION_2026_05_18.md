# Floor-Preserving Domain Lift Sufficient Condition

Status: `CONDITIONAL_LIFT_SUFFICIENT_CONDITION_ONLY`

Global verdict preserved: `OPEN`

This file adds a sufficient condition for the second sink: if a floor-preserving domain lift exists, then the finite-support uniform-floor certificate transfers to the admissible-domain target.

## Lean module

`Chronos.Frontier.FloorPreservingDomainLiftSufficientCondition`

## Formal object

- `FloorPreservingDomainLift`

## Closed conditional theorems

- `floor_preserving_domain_lift_to_uniform_floor`
- `floor_preserving_domain_lift_to_admissible_lift`
- `floor_preserving_domain_lift_resolves_second_sink`

## Conditional input

`FloorPreservingDomainLift`

Minimal form:

`Each admissible target-domain fiber maps back to an admissible finite-domain fiber with no larger mass.`

## Boundary

Does not prove:

- existence of `FloorPreservingDomainLift`
- unconditional `FiniteSupportToAdmissibleDomainLift`
- absence of `FiniteSupportLiftFailureCountermodel`
- unrestricted `UniversalFiberEntropyGap`
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem
