# Newstein Non-Tree-Edge Fundamental Cycle Lemma

Status: CONDITIONAL

## Status
CONDITIONAL

## Deduction

This file is conditionally discharged by `docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md`.

Fix a spanning tree \(T\) in the rooted local complex \(L\). For every non-tree edge \(e=uv\), define
\[
C_e := e + P_T(u,v),
\]
where \(P_T(u,v)\) is the unique tree path joining \(u\) and \(v\).

Under the rooted-local path hypothesis recorded in `docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md`, the path \(P_T(u,v)\) is rooted-local, hence \(C_e\) is a rooted-local cycle. Therefore every non-tree edge determines a rooted-local fundamental cycle.

## Finish condition

Replace this conditional deduction by a proof from repository-native lemmas.
