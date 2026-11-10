# Finite cycle locality: formal status checkpoint (2026-11-09)

Scope: a `Z/2` edge connection on a finite cycle, with independently
gauge-quotiented proper path windows when `3 <= n` and `2*r+1 < n`.
The global cycle XOR distinguishes zero and single-twist connections.
**Vacuity boundary:** every pair of edge-bit assignments on such a path
is gauge-equivalent; `LocalEquiv` therefore imposes no transport constraint.
Its `localSummary = n` tests compare metadata fields, not graph invariants.
This is a path-gauge non-rigidity witness, not a local reconstruction theorem.

## Mac kernel receipts (Lean 4.29.0)

- `LocalityHolonomySeparation.lean`: three named load-bearing declarations
  were kernel checked, including private auxiliary proofs used by them;
  axiom audit PASS. The *original* Mac candidate (before comment-only
  documentation changes) had SHA-256
  `572c54e33387c65ff452d567f89b126ec0b2e63805a857c80e6431788aede803`.
  The pre-review PR blob was `2445ce0f89b84604c653730affdbd2c3e7b1ce55`;
  do not interpret that original candidate SHA-256 as the revised PR blob.
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

## Integrated verification checkpoint and remaining obligations

- At PR HEAD `77e70cc3e456f638cd264438a9c01f3a2f2afe36`,
  the Mac source-blob audit, independent imported-module compilation, and
  `#print axioms` audit of **13 named theorems** all passed under Lean 4.29.0;
  only `propext`, `Classical.choice`, and `Quot.sound` were reported.
  Private helper declarations are compiled as dependencies of those theorems.
- The full repository `lake build` step passed in GitHub CI at that PR HEAD;
  the remaining overall CI jobs and CodeRabbit review must be assessed
  separately at each new exact HEAD.
- The review correction here changes only documentation/comments, not
  theorem statements or proof terms. A new exact-head validation is still
  required before merge.
- **Scope/vacuity inspection: PASS with limitation.** Path gauge existence is
  automatic for arbitrary edge labels; the `LocalEquiv` part is not a
  nontrivial local obstruction. Its metadata equality does not certify any
  geometric property. The nontrivial distinction used here is global XOR.
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

Merge only after current exact-HEAD module/build checks, axiom audit
(no `sorryAx`), the above scope/vacuity disclosure, and required repository
CI/review gates pass. Do not promote broader graph-ball or physics claims.
Preserve the original Mac HEAD/branch/working tree and temporary checkpoints.
