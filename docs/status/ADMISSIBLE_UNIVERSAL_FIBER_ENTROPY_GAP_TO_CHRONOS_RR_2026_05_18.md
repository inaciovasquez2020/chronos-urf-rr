# Admissible Universal Fiber-Entropy Gap to Chronos-RR — 2026-05-18

## Status

`ADMISSIBLE_CHRONOS_RR_TARGET_CLOSED_RESTRICTED_ONLY`

## Target

`AdmissibleUniversalFiberEntropyGapToChronosRR`

## Exact Chronos-RR Target

`ChronosRRTarget M` consists of:

- the closed order surface;
- a positive `epsilon`;
- a Chronos-RR floor:
  `∀ n : ℕ, epsilon ≤ M.fiberMass n`.

## Closed Bridge

The Lean module

`Chronos.Frontier.AdmissibleUniversalFiberEntropyGapToChronosRR`

proves:

- `chronosRRTarget_from_universalFiberEntropyGapTarget`
- `UniversalFiberEntropyGapToChronosRRBridge_solved`
- `AdmissibleUniversalFiberEntropyGapToChronosRR_solved`
- `AdmissibleChronosRRTarget_solved`
- `UnrestrictedChronosRRTarget_refuted`

## Refuted Unrestricted Target

For arbitrary `FiberMassData`, the unrestricted target is refuted by the zero fiber-mass object:

`zeroFiberMassData`

## Boundary

Admissible restricted Chronos-RR target only.

The unrestricted arbitrary-`FiberMassData` Chronos-RR target is refuted.

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
