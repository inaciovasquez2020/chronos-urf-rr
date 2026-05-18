# Admissible Fiber-Mass Uniform Floor — 2026-05-18

## Status

`ADMISSIBLE_FIBER_MASS_FLOOR_CLOSED_RESTRICTED_ONLY`

## Target

`AdmissibleFiberMassUniformFloor`

## Context

PR #362 refuted the unrestricted statement:

`UniversalWeakestMissingMeasureFiberMassLemma`

for arbitrary `FiberMassData`.

The admissible replacement is therefore not:

`∀ M : FiberMassData, FiberMassUniformFloor M`

but instead a restricted structure carrying the floor as certified data:

`AdmissibleFiberMassData`

## Closed Declarations

The Lean module

`Chronos.Frontier.AdmissibleFiberMassUniformFloor`

proves:

- `AdmissibleFiberMassUniformFloor_solved`
- `AdmissibleRateThickFiberCoercivityTarget_solved`
- `AdmissibleFiberMassData_nonempty`

## Rebuilt Theorem

For every admissible fiber-mass object:

`A : AdmissibleFiberMassData`

the rate-thick fiber coercivity target closes for `A.data`:

`Nonempty (RateThickFiberCoercivityTarget A.data)`

## Boundary

Admissible restricted fiber-mass floor only.

The uniform floor is packaged as admissible data, not proved for arbitrary `FiberMassData`.

Does not prove:

- unrestricted `RateThickFiberCoercivity`
- unrestricted `UniversalFiberEntropyGap`
- unrestricted Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem

Exact verifier boundary tokens:

- does not prove unrestricted RateThickFiberCoercivity
- does not prove unrestricted UniversalFiberEntropyGap
- does not prove unrestricted Chronos-RR
- does not prove H4.1/FGL
- does not prove P vs NP
- does not prove any Clay problem
