# Newstein Exact Cycle-Generation Closure Target

Status: OPEN

## Statement

Let \(L\) be the rooted local complex and let \(T\subseteq L\) be a spanning tree. For every non-tree edge \(e\in E(L)\setminus E(T)\), let \(P_T(e)\) denote the unique tree path in \(T\) joining the endpoints of \(e\), and define the fundamental cycle
\[
C_e := e + P_T(e).
\]

## Exact closure target

The exact closure target is:

1. each \(C_e\) is rooted-local;
2. each \(C_e\) belongs to the rooted-local generating family;
3. the family \(\{C_e : e\in E(L)\setminus E(T)\}\) generates the full local cycle space \(Z_1(L)\).

## Consequence

A proof of this statement closes:

- `docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md`
- `docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_PROOF_BLUEPRINT.md`
- `docs/math/NEWSTEIN_NON_TREE_EDGE_FUNDAMENTAL_CYCLE_LEMMA.md`

## Status

OPEN

## Finish condition

Replace this file by a proof, or by a proof-complete decomposition into strictly weaker proved lemmas whose conjunction implies the statement above.
