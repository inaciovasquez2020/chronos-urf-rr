# Conditional Frontier Status — 2026-04-27

Status: Conditional / Frontier Formalization

This repository contains a large formalization surface for Chronos/URF-style rigidity ideas.
It is not yet an unconditional proof repository while project axioms, admits, or sorries remain.
Files containing `sorry`, `admit`, or project axioms are frontier or conditional files and must not be cited as verified root theorems until discharged.

Axiom count: 7
Admit count: 4
Sorry count: 4

## Axiom locations

- `lean/tests/newstein_local_coboundary_block.lean:10` — `axiom geodesic_to_tree_path :`
- `lean/tests/newstein_local_coboundary_block.lean:13` — `axiom tree_path_to_fundamental_cycle :`
- `lean/tests/newstein_local_coboundary_block.lean:16` — `axiom fundamental_cycle_to_local_coboundary :`
- `lean/Oblivion/Cycle.lean:15` — `axiom cycle_length_le_twoR_of_subgraph_ball`
- `urf-core/urf_law3.lean:15` — `axiom capacity :`
- `urf-core/urf_law3.lean:19` — `axiom chain_rule :`
- `urf-core/urf_law3.lean:25` — `axiom cmi_nonneg :`

## Admit locations

- `lean/Oblivion/CycloneSignedLift.lean:30` — `admit`
- `lean/Oblivion/CycloneSignedLift.lean:39` — `admit`
- `lean/Oblivion/CycloneSignedLift.lean:53` — `· admit`
- `urf-core/urf_law3.lean:37` — `admit`

## Sorry locations

- `URF/Canonical/lean_urf_nonfactorization.lean:13` — `sorry`
- `URF/Canonical/lean_urf_nonfactorization.lean:16` — `sorry`
- `URF/Canonical/lean_urf_nonfactorization.lean:19` — `sorry`
- `URF/Canonical/lean_urf_nonfactorization.lean:26` — `sorry`

## Boundary rule

If `axiom + admit + sorry > 0`, no unconditional Chronos/URF theorem-closure claim is allowed.
