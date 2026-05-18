# Finite Positive Fiber-Mass Uniform Floor — 2026-05-18

## Status

`FINITE_POSITIVE_FIBER_MASS_UNIFORM_FLOOR_CLOSED`

## Target

`FinitePositiveFiberMassUniformFloorTheorem`

## Theorem

For a finite nonempty fiber index type `Fin N`, if every fiber mass is strictly positive, then there exists a positive uniform lower floor.

Formally:

`0 < N → (∀ i : Fin N, 0 < M.mass i) → ∃ ε > 0, ∀ i : Fin N, ε ≤ M.mass i`

## Closed Declarations

The Lean module

`Chronos.Frontier.FinitePositiveFiberMassUniformFloor`

proves:

- `finite_positive_fiber_mass_uniform_floor`
- `FinitePositiveFiberMassUniformFloorTheorem_solved`

## Boundary

Finite fiber-mass compactness theorem only.

This does not prove unrestricted `FiberMassUniformFloor` for arbitrary `FiberMassData`; that unrestricted route was already refuted.

Does not prove:

- unrestricted `RateThickFiberCoercivity`
- unrestricted `UniversalFiberEntropyGap`
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem

Does not refute:

- P vs NP
- any Clay problem

Exact verifier boundary tokens:

- does not prove unrestricted FiberMassUniformFloor for arbitrary FiberMassData
- does not prove unrestricted RateThickFiberCoercivity
- does not prove unrestricted UniversalFiberEntropyGap
- does not prove unrestricted Chronos-RR
- does not prove unrestricted H4.1/FGL
- does not prove P vs NP
- does not refute P vs NP
- does not prove any Clay problem
- does not refute any Clay problem
