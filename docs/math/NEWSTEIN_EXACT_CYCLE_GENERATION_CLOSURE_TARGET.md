# Newstein Exact Cycle-Generation Closure Target

Status: CONDITIONAL

## Statement

Let \(L\) be a connected rooted local complex, let \(T\subseteq L\) be a spanning tree, and assume:

1. for every non-tree edge \(e=uv\in E(L)\setminus E(T)\), the unique tree path \(P_T(u,v)\) is rooted-local in \(L\);
2. cycles are taken over \(\mathbf F_2\).

Define, for each \(e\in E(L)\setminus E(T)\), the fundamental cycle
\[
C_e := e + P_T(u,v)\in C_1(L;\mathbf F_2).
\]

Then:

\[
\{C_e : e\in E(L)\setminus E(T)\}\subseteq Z_1(L;\mathbf F_2),
\]
the family \(\{C_e : e\in E(L)\setminus E(T)\}\) is linearly independent, spans \(Z_1(L;\mathbf F_2)\), and forms a rooted-local generating family, and
\[
Z_1(L;\mathbf F_2)=\operatorname{span}_{\mathbf F_2}\{C_e : e\in E(L)\setminus E(T)\}.
\]

## Dependency

This controller is conditional exactly on `docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md`.

## Conditional closure hypothesis

The rooted-local path hypothesis above is the remaining conditional input.

## Conditional consequence

Conditional on the rooted-local path hypothesis above, this controller surface discharges:

- `docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md`
- `docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_PROOF_BLUEPRINT.md`
- `docs/math/NEWSTEIN_NON_TREE_EDGE_FUNDAMENTAL_CYCLE_LEMMA.md`

## Status

CONDITIONAL

## Finish condition

Replace the rooted-local path hypothesis by a proved repository-native lemma.
