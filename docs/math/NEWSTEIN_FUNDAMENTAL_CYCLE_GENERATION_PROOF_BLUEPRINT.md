# Newstein Fundamental Cycle Generation Proof Blueprint

Status: PROVED

## Goal

Refine `docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md` into a proof-complete theorem decomposition.

## Link to exact closure target

This blueprint is controlled by `docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md`.

## Status
PROVED

### 1. Local spanning-tree reduction

Choose a spanning tree \(T\subseteq L\).

### 2. Non-tree-edge cycle generation

For every non-tree edge \(e=uv\), define
\[
C_e := e + P_T(u,v).
\]

### 3. Triangle reduction step

By `docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md`, each path \(P_T(u,v)\) is rooted-local. By `docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md`, each rooted-local fundamental cycle lies in the rooted-local generating family.

### 4. Rooted-local generating family

This produces a rooted-local generating family for the local cycle space.

### 5. Export step

By `docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md`, the family \(\{C_e : e\in E(L)\setminus E(T)\}\) spans \(Z_1(L;\mathbf F_2)\).

## Finish condition

Closed by proved controller and dependency lemma.
