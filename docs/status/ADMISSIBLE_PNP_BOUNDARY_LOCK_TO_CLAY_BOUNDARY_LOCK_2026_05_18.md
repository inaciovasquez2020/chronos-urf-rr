# Admissible P vs NP Boundary Lock to Clay Boundary Lock — 2026-05-18

## Status

`ADMISSIBLE_CLAY_BOUNDARY_LOCK_CLOSED_NO_THEOREM_PROMOTION`

## Target

`AdmissiblePNPBoundaryLockToClayBoundaryLock`

## Exact Boundary Target

`ClayBoundaryLockTarget M` consists of:

- `Nonempty (PNPBoundaryLockTarget M)`;
- `ClayStatus.frontier_open`;
- proof that the status is locked as `frontier_open`.

## Closed Bridge

The Lean module

`Chronos.Frontier.AdmissiblePNPBoundaryLockToClayBoundaryLock`

proves:

- `clayBoundaryLockTarget_from_pnpBoundaryLockTarget`
- `PNPBoundaryLockToClayBoundaryLockBridge_solved`
- `AdmissiblePNPBoundaryLockToClayBoundaryLock_solved`
- `AdmissibleClayBoundaryLockTarget_solved`
- `clay_boundary_status_frontier_open`

## Boundary

Admissible restricted Clay boundary lock only.

This records `ClayStatus.frontier_open` only.

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

- does not prove unrestricted RateThickFiberCoercivity
- does not prove unrestricted UniversalFiberEntropyGap
- does not prove unrestricted Chronos-RR
- does not prove unrestricted H4.1/FGL
- does not prove P vs NP
- does not refute P vs NP
- does not prove any Clay problem
- does not refute any Clay problem
