# Universal Measure/Fiber-Mass Lemma Refutation — 2026-05-18

## Status

`UNRESTRICTED_MEASURE_FIBER_MASS_LEMMA_REFUTED_RESTRICTED_TARGET_CLOSED`

## Refuted Target

The unrestricted lemma isolated by PR #361 is false for arbitrary `FiberMassData`:

`UniversalWeakestMissingMeasureFiberMassLemma`

The counterexample is:

`zeroFiberMassData`

with

`fiberMass n = 0`

for all `n : ℕ`.

Therefore no positive `epsilon` can satisfy:

`∀ n : ℕ, epsilon ≤ fiberMass n`.

## Closed Declarations

The Lean module

`Chronos.Frontier.UniversalWeakestMissingMeasureFiberMassLemmaRefutation`

proves:

- `zeroFiberMassData_no_uniform_floor`
- `UniversalWeakestMissingMeasureFiberMassLemma_refuted`
- `UnrestrictedRateThickFiberCoercivityTarget_refuted`
- `RestrictedMeasureFiberMassFloorTarget_solved`

## Rebuilt Theorem

The admissible restricted target is closed:

`RestrictedMeasureFiberMassFloorTarget`

meaning:

`∀ M : FiberMassData, FiberMassUniformFloor M → Nonempty (RateThickFiberCoercivityTarget M)`

## Boundary

This refutes only the unrestricted arbitrary-`FiberMassData` universal floor.

It closes only the restricted target assuming `FiberMassUniformFloor M`.

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
