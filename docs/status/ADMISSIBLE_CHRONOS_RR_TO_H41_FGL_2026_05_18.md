# Admissible Chronos-RR to H4.1/FGL — 2026-05-18

## Status

`ADMISSIBLE_H41_FGL_TARGET_CLOSED_RESTRICTED_ONLY`

## Target

`AdmissibleChronosRRToH41FGL`

## Exact H4.1/FGL Target

`H41FGLTarget M` consists of:

- the closed order surface;
- a positive `epsilon`;
- an H4.1/FGL floor:
  `∀ n : ℕ, epsilon ≤ M.fiberMass n`.

## Closed Bridge

The Lean module

`Chronos.Frontier.AdmissibleChronosRRToH41FGL`

proves:

- `h41FGLTarget_from_chronosRRTarget`
- `ChronosRRToH41FGLBridge_solved`
- `AdmissibleChronosRRToH41FGL_solved`
- `AdmissibleH41FGLTarget_solved`
- `UnrestrictedH41FGLTarget_refuted`

## Refuted Unrestricted Target

For arbitrary `FiberMassData`, the unrestricted target is refuted by the zero fiber-mass object:

`zeroFiberMassData`

## Boundary

Admissible restricted H4.1/FGL target only.

The unrestricted arbitrary-`FiberMassData` H4.1/FGL target is refuted.

Does not prove:

- unrestricted `RateThickFiberCoercivity`
- unrestricted `UniversalFiberEntropyGap`
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem

Exact verifier boundary tokens:

- does not prove unrestricted RateThickFiberCoercivity
- does not prove unrestricted UniversalFiberEntropyGap
- does not prove unrestricted Chronos-RR
- does not prove unrestricted H4.1/FGL
- does not prove P vs NP
- does not prove any Clay problem
