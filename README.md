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

External position:
- `docs/status/EXTERNAL_POSITION_2026_04_23.md`

## Theorem Layer

INCOMPLETE

finite-patch H4.1 is conditional only on `proofs/Chronos/conditional/FGL_PROOF_SHELL_2026_04.md`.

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

## Formal Status

Status: Conditional / Frontier Formalization

Build status:
- A successful build means the checked root target compiles.
- It does not imply that axiom-dependent, admit-dependent, or sorry-dependent results prove their headline targets.

Theorem status:
- This repository currently contains project-defined `axiom` declarations, `admit` proof holes, and `sorry` proof holes.
- `axiom` is a trusted assumption, not a proof.
- `admit` is a proof hole.
- `sorry` is a proof hole.
- Any result depending on project axioms, admits, or sorries is Conditional.

Current status:
- Strongest verified theorem: none asserted at repository level
- Weakest missing theorem: split the verified root from conditional/frontier modules, then discharge or quarantine every load-bearing axiom/admit/sorry
- Conditional inventory: `docs/status/CONDITIONAL_FRONTIER_STATUS_2026_04_27.md`

## External status

This repository is governed by [`docs/status/EXTERNAL_STATUS_LOCK.md`](docs/status/EXTERNAL_STATUS_LOCK.md). Build success, CI success, dashboards, ledgers, axioms, admits, `sorry`, or placeholder witnesses do not constitute theorem-level closure.

## Lean proof portfolio classification

This repository is governed by [`docs/status/LEAN_PROOF_PORTFOLIO_CLASSIFICATION.md`](docs/status/LEAN_PROOF_PORTFOLIO_CLASSIFICATION.md). Its role in the portfolio is explicitly classified as proof-facing, conditional frontier, infrastructure/documentation, or legacy/scaffold.
