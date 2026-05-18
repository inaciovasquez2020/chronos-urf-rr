# Terminal Admissible Boundary-Chain Certificate — 2026-05-18

## Status

`TERMINAL_ADMISSIBLE_BOUNDARY_CHAIN_CERTIFICATE_CLOSED_NO_THEOREM_PROMOTION`

## Target

`TerminalAdmissibleBoundaryChainCertificate`

## Exact Certificate

For every admissible fiber-mass object:

`A : AdmissibleFiberMassData`

there exists a Clay boundary lock certificate:

`C : ClayBoundaryLockTarget A.data`

with

`C.status = ClayStatus.frontier_open`.

## Closed Declarations

The Lean module

`Chronos.Frontier.TerminalAdmissibleBoundaryChainCertificate`

proves:

- `terminalCertificate_from_clayBoundaryLockTarget`
- `TerminalAdmissibleBoundaryChainCertificate_solved`
- `TerminalBoundaryChainAudit_solved`

## Chain Certified

The terminal certificate packages the admissible chain:

`AdmissibleFiberMassData`
→ `RateThickFiberCoercivityTarget`
→ `UniversalFiberEntropyGapTarget`
→ `ChronosRRTarget`
→ `H41FGLTarget`
→ `PNPBoundaryLockTarget`
→ `ClayBoundaryLockTarget`

## Boundary

Terminal admissible boundary-chain certificate only.

This records `PNPStatus.frontier_open` only.

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
