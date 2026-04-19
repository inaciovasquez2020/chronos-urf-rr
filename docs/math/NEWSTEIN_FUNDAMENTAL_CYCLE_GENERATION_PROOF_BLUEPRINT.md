# Newstein Fundamental Cycle Generation Proof Blueprint

Status: CONDITIONAL

## Goal

Refine `docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md` into a proof-complete theorem decomposition.

## Link to exact closure target

This blueprint is controlled by `docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md`.

## Status
CONDITIONAL

### 1. Local spanning-tree reduction

Choose a spanning tree \(T\subseteq L\).

### 2. Non-tree-edge cycle generation

For every non-tree edge \(e=uv\), define
\[
C_e := e + P_T(u,v).
\]

### 3. Triangle reduction step

Under the controller hypothesis, each rooted-local fundamental cycle lies in the rooted-local generating family.

### 4. Rooted-local generating family

This produces a rooted-local generating family for the local cycle space.

Weakest missing sublemma: the rooted-local path hypothesis implies that the fundamental cycle attached to each non-tree edge lies in the rooted-local generating family.

### 5. Export step

Under the controller hypothesis, the family \(\{C_e : e\in E(L)\setminus E(T)\}\) spans \(Z_1(L;\mathbf F_2)\).

## Finish condition

Replace this conditional blueprint by a proof or a proof-complete theorem decomposition for the fundamental cycle-generation sublemma.
