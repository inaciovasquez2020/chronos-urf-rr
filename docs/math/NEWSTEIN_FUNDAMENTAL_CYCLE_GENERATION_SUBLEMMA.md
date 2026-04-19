# Newstein Fundamental Cycle Generation Sublemma

Status: PROVED

## Target statement

For the rooted local complex \(L\) with a chosen spanning tree \(T\), every non-tree edge \(e\) determines a rooted-local fundamental cycle \(C_e\), each such \(C_e\) lies in the rooted-local generating family, and the family \(\{C_e : e \notin T\}\) generates the full local cycle space \(Z_1(L)\).

## Exact closure target

This file is controlled by `docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md`.

## Deduction target

By `docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md`, each path \(P_T(u,v)\) is rooted-local. By `docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md`, the cycles \(C_e\) are rooted-local, lie in the rooted-local generating family, and form a basis of \(Z_1(L;\mathbf F_2)\).

Therefore the fundamental cycle-generation sublemma holds.

## Status
PROVED

## Finish condition

Closed by deduction from proved repository-native lemmas.
