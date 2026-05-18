# Admissible H4.1/FGL to P vs NP Boundary Lock — 2026-05-18

## Status

`ADMISSIBLE_PNP_BOUNDARY_LOCK_CLOSED_NO_THEOREM_PROMOTION`

## Target

`AdmissibleH41FGLToPNPBoundaryLock`

## Exact Boundary Target

`PNPBoundaryLockTarget M` consists of:

- `Nonempty (H41FGLTarget M)`;
- `PNPStatus.frontier_open`;
- proof that the status is locked as `frontier_open`.

## Closed Bridge

The Lean module

`Chronos.Frontier.AdmissibleH41FGLToPNPBoundaryLock`

proves:

- `pnpBoundaryLockTarget_from_h41FGLTarget`
- `H41FGLToPNPBoundaryLockBridge_solved`
- `AdmissibleH41FGLToPNPBoundaryLock_solved`
- `AdmissiblePNPBoundaryLockTarget_solved`
- `pnp_boundary_status_frontier_open`

## Boundary

Admissible restricted P vs NP boundary lock only.

This records `PNPStatus.frontier_open` only.

Does not prove:

- unrestricted `RateThickFiberCoercivity`
- unrestricted `UniversalFiberEntropyGap`
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem

Does not refute:

- P vs NP

Exact verifier boundary tokens:

- does not prove unrestricted RateThickFiberCoercivity
- does not prove unrestricted UniversalFiberEntropyGap
- does not prove unrestricted Chronos-RR
- does not prove unrestricted H4.1/FGL
- does not prove P vs NP
- does not refute P vs NP
- does not prove any Clay problem
