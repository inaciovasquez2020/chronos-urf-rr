# Formal Status — 2026-04-27

Status: Conditional / Frontier Formalization

## Build status

The repository builds, but build success is not theorem verification.

## Theorem status

This repository currently contains project-defined axioms, admitted obligations, and `sorry` proof holes.

- `axiom` is a trusted assumption, not a proof.
- `admit` is a proof hole.
- `sorry` is a proof hole.
- Any result depending on project axioms, admits, or sorries is Conditional.
- No dependency on these assumptions should be described as proved, closed, final, terminal, unconditional, or machine-verified.

## Current status

- Current classification: Conditional / Frontier Formalization
- Strongest verified theorem: none asserted at repository level
- Weakest missing theorem: split the verified root from conditional/frontier modules, then discharge or quarantine every load-bearing axiom/admit/sorry
- Conditional inventory: `docs/status/CONDITIONAL_FRONTIER_STATUS_2026_04_27.md`

## Boundary rule

If `axiom + admit + sorry > 0`, no unconditional Chronos/URF theorem-closure claim is allowed.


## Source-level proof-hole closure update — 2026-04-27

Status: Proved for source-level axiom/admit/sorry elimination.

Verified:
- `rg -n '^\s*(axiom|admit|sorry)\b' lean URF urf-core` returns no source-level proof holes.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q` passes with 384 tests.
- `lake build` passes.

Scope:
This closes the source-hole inventory only.

It does not prove general H4.1, general FGL row-separation, R1/R2/R3, or unconditional Chronos/URF theorem-level closure.

Current theorem-level status:
- Petersen 2-lift finite-instance FGL certificate: Proved.
- General H4.1: Conditional.
- General FGL row-separation: Conditional.

