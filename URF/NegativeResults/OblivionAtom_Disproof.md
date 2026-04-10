# Oblivion Atom Disproof

## Lean Status
This file is paired with `URF/Lean/OblivionAtom_Disproof.lean`.

## Formalization policy
The Lean module is intentionally buildable while isolating every unresolved mathematical step as a named axiom.

## Axiom inventory
1. `Gr_locally_homogeneous`
2. `Gr_degree_bounded`
3. `Gr_girth_bound`
4. `quotientRank_eq_localTwoComplexH1Rank`
5. `localTwoComplexH1Rank_growth`
6. `W5_parameters`
7. `W5_local_homogeneity`
8. `W5_rank_separation`

## Current theorem
The module proves:
- existence of a fixed-parameter counterexample family,
- impossibility of a uniform quotient-rank bound,
- W(5)-level global separation,

conditional on the named axioms above.

## Micro-fix workflow
Replace exactly one axiom at a time with a theorem and rebuild.
