# Admissible Rate-Thick to Universal Fiber-Entropy Gap — 2026-05-18

## Status

`ADMISSIBLE_UNIVERSAL_FIBER_ENTROPY_GAP_TARGET_CLOSED_RESTRICTED_ONLY`

## Target

`AdmissibleRateThickFiberCoercivityToUniversalFiberEntropyGap`

## Exact Gap Target

`UniversalFiberEntropyGapTarget M` consists of:

- the closed order surface;
- a positive `epsilon`;
- a uniform entropy-gap floor:
  `∀ n : ℕ, epsilon ≤ M.fiberMass n`.

## Closed Bridge

The Lean module

`Chronos.Frontier.AdmissibleRateThickToUniversalFiberEntropyGap`

proves:

- `universalFiberEntropyGapTarget_from_rate_thick_target`
- `RateThickToUniversalFiberEntropyGapBridge_solved`
- `AdmissibleRateThickFiberCoercivityToUniversalFiberEntropyGap_solved`
- `AdmissibleUniversalFiberEntropyGapTarget_solved`
- `UnrestrictedUniversalFiberEntropyGapTarget_refuted`

## Refuted Unrestricted Target

For arbitrary `FiberMassData`, the unrestricted target is refuted by the zero fiber-mass object:

`zeroFiberMassData`

## Boundary

Admissible restricted universal fiber-entropy gap target only.

The unrestricted arbitrary-`FiberMassData` universal fiber-entropy target is refuted.

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
