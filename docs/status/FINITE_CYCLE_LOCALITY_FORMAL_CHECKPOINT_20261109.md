# Finite cycle locality: formal status checkpoint (2026-11-09)

Scope: a `Z/2` edge connection on a finite simple cycle, with independently
gauge-quotiented radius-`r` neighborhoods, provided `3 <= n` and
`2*r+1 < n`. Global cycle XOR distinguishes zero and single-twist connections.

## Mac kernel receipts (Lean 4.29.0)

- `LocalityHolonomySeparation.lean`: three load-bearing declarations compiled;
  axiom audit PASS, permitted axioms only. SHA-256 source
  `572c54e33387c65ff452d567f89b126ec0b2e63805a857c80e6431788aede803`.
- `CycleArcBallWindowBridge.lean`: three declarations compiled;
  axiom audit PASS; SHA-256
  `3727195ceb3baf8d95dc7dd9e7a5028371c06a5bd14f069e2735e1112de35d12`.
- `CycleWalkReachabilityBridge.lean`: four declarations compiled;
  axiom audit PASS; SHA-256
  `0315efdcbc18ce77c8067c16ae2d3610517f045e8d4caca57311c870b8ae5846`.
- `CycleGraphReachabilityBridge.lean`: two declarations compiled as a concatenated
  temporary source with precisely the verified graph-path proof body;
  axiom audit PASS; original appended body SHA-256
  `dc709bca3f802b95810eee73fbc530a9c124ce8599c449d983ad29ec821180c5`.
- Allowed axioms in all audited proofs: `propext`, `Classical.choice`,
  `Quot.sound`. The original `sorryAx` arose only in failed intermediate builds.

## New integration obligations

- Import-based compilation of each module and `Oblivion.CycleGraphWindowBridge`
  has not yet been audited on the Mac. `graphBall_iff_window` is a new
  composition theorem and must undergo compilation plus `#print axioms`.
- The broad `lake build` of Chronos is not claimed to have passed at this
  revision. Repository dependencies can have unrelated existing failures.
- The proved graph model uses residue-labeled vertices and explicit
  clockwise/counterclockwise edge steps. It does not verify that Chronos's
  preexisting placeholder `Oblivion.ball`, `RootedBallCode`, or FMT-style
  graph interfaces have correct semantics.
- The correspondence between oriented `Nat` edge labels in `LocalEquiv`
  and the independent `Int` residue graph-edge representation is not
  yet formally established. Therefore the theorem does not certify every
  desired representation-level equivalence across the repository.
- No finite result or holonomy identity proves a physically necessary
  fifth dimension or cosmological observational distinction.

## Stop/promotion policy

Keep this change in draft until the exact PR HEAD passes module builds,
axiom audits (no `sorryAx`), scope/vacuity inspection, and repository CI.
Do not merge with unresolved required checks. Preserve the original Mac
HEAD/branch/working tree and verified temporary checkpoints.
