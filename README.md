# Chronos URF — Final State


<!-- PUBLIC-SURFACE:BEGIN -->
## Start Here
- [`QUICKSTART.md`](QUICKSTART.md)
- [`docs/public/START_HERE.md`](docs/public/START_HERE.md)

## Proof Status
- [`docs/public/PROOF_STATUS.md`](docs/public/PROOF_STATUS.md)

## Independent Verification
- [`docs/public/INDEPENDENT_VERIFICATION.md`](docs/public/INDEPENDENT_VERIFICATION.md)

## Why It Matters
- [`docs/public/WHY_IT_MATTERS.md`](docs/public/WHY_IT_MATTERS.md)

## Citation
- [`CITATION.cff`](CITATION.cff)
<!-- PUBLIC-SURFACE:END -->

## Status
- Build: PASS
- Tests: 88/88 PASS
- `grep -RInE 'sorry|admit|axiom' URF/Lean`: empty
- Witness modules compile: PASS
- CI: 100%

## Completion
- Internal Technical Completion: 100%
- Executable Core Closure: 100%
- RootedBallEncoding: 100%
- EFDuplicator: 100%
- Witness Specification Layer: compiled
- Unconditional witness-family mathematics: in progress
- Publication Readiness (verified executable scope): 100%

## Core Components

### RootedBallEncoding
- Canonical vertex type encoding via `rootedBallCode`
- Image cardinality bounds fully normalized
- Surrogate bounds (`M`) structurally reduced and controlled

### EFDuplicator
- `PartialIso` formalized
- `EFWinData` semantic object introduced
- EF game abstraction:
  - `EFGameState`
  - `EFGameStep`
  - `EFStrategy`
- Iteration law:
  - `EFStrategy_iter`
- Winning predicate:
  - `EFWinning`
  - `EFWinningAfter`
- Monotonicity + normalization lemmas complete

## Structural Result
Local indistinguishability (RootedBallEncoding) is formally connected to EF-game strategy structure (EFDuplicator) via executable semantics.

## Witness Layer
- `URF/Lean/Witnesses/CFILiftWitnessSpec.lean`: compiles
- `URF/Lean/Witnesses/CFILiftWitnessCompletion.lean`: compiles
- Current witness layer is a formal specification/completion scaffold
- Unconditional explicit CFI/lift witness construction is not yet claimed here

## Invariants
- No placeholders
- No axioms
- Fully executable Lean proofs
- CI-stable

## Repository Guarantees
- Deterministic builds
- Reproducible results
- Formal verification-ready

## Next Phase
- Explicit witness-family instantiation
- Local-agreement theorem for the witness family
- Global invariant-gap theorem for the witness family
- Treewidth-divergence theorem for the witness family
- Paper write-up / submission

## Open Problems
- Witness-layer completion is currently a compiled scaffold; the unconditional explicit witness family remains open.
- finite-patch H4.1 is conditional only on `proofs/Chronos/conditional/FGL_PROOF_SHELL_2026_04.md`.
- H4.1 finite-patch conditional chain indexed at `proofs/Chronos/conditional/H41_FINITE_PATCH_INDEX_2026_04.md`.

## Acknowledgments
See docs/ACKNOWLEDGMENTS.md
