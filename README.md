# Chronos URF — Conditional Executable Reference

## Repository Status

CONDITIONAL

## Executable Layer

* Build: PASS
* Tests: 88/88 PASS
* `grep -RInE 'sorry|admit|axiom' URF/Lean`: empty
* Witness modules compile: PASS
* CI: 100%

## Scope

* Deterministic verification scaffolds
* Reproducible executable artifact surface
* Formal Lean proof surface for the assembly layer

## Theorem Layer

INCOMPLETE

Terminal open theorem-level inputs remain exactly:

* (R1) Long-Chord Exclusion Lemma
* (R2) Diameter-Separation Filling Obstruction
* (R3) Uniform Local-Type Capacity Lemma

## Correct dependency form

    (R1) ──► dim(W^tw/W^triv) = 2
    (R2) ──► cross-fiber injectivity
    (R2) + (R1) + sigma-package assembly ──► dim(Z₁/W^glob) ≥ 2|U|
    (R3) + (dim(Z₁/W^glob) ≥ 2|U|) + (|U| → ∞) ──► non-factorization

## Non-claims

* No unconditional theorem-level closure is claimed here.
* No further theorem-level closure is possible without new mathematical input on (R1), (R2), (R3).

## Routing

* Canonical URF definitions and dependency ledgers remain in `urf-core`.
* This repository remains the executable reference surface.

