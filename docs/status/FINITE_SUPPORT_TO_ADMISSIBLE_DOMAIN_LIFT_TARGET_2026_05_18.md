# Finite-Support to Admissible-Domain Lift Target

Status: `OPEN_LIFT_TARGET_SURFACE_ONLY`

Global verdict preserved: `OPEN`

This file formalizes the second global URF sink: lifting the finite-support uniform-floor route into the intended admissible domain.

## Lean module

`Chronos.Frontier.FiniteSupportToAdmissibleDomainLiftTarget`

## Formal objects

- `FiniteSupportToAdmissibleDomainLift`
- `FiniteSupportLiftFailureCountermodel`

## Closed surface theorems

- `finite_support_lift_transfers_floor`
- `finite_support_lift_resolves_admissible_sink`
- `finite_support_lift_failure_countermodel_excludes_lift`

## Weakest missing object

`FiniteSupportToAdmissibleDomainLift`

Minimal form:

`FiniteSupportUniformFloorCertificate Dfinite implies UniformPositiveFiberMassFloor Dadm`

## Countermodel alternative

`FiniteSupportLiftFailureCountermodel`

Minimal form:

`FiniteSupportUniformFloorCertificate Dfinite together with NoUniformPositiveFiberMassFloorCountermodel Dadm`

## Boundary

Does not prove:

- existence of `FiniteSupportToAdmissibleDomainLift`
- absence of `FiniteSupportLiftFailureCountermodel`
- unrestricted `UniversalFiberEntropyGap`
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem
