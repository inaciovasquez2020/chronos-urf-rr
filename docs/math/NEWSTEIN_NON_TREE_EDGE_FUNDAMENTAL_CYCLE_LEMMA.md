# Newstein Non-Tree-Edge Fundamental Cycle Lemma

Status: PROVED

## Status
PROVED

## Deduction

This file is discharged by `docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md`.

Fix a spanning tree \(T\) in the rooted local complex \(L\). For every non-tree edge \(e=uv\), define
\[
C_e := e + P_T(u,v),
\]
where \(P_T(u,v)\) is the unique tree path joining \(u\) and \(v\).

By `docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md`, the path \(P_T(u,v)\) is rooted-local. By `docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md`, \(C_e\) is therefore a rooted-local cycle. Hence every non-tree edge determines a rooted-local fundamental cycle.

## Finish condition

Closed by deduction from proved repository-native lemmas.
