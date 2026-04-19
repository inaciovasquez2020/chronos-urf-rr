# Newstein Fundamental Cycle Generation Proof Blueprint

Status: OPEN

## Goal

Refine `docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md` into a proof-complete theorem decomposition.

## Link to exact closure target

This blueprint is controlled by `docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md`.

## Status
OPEN

### 1. Local spanning-tree reduction

Choose a spanning tree in the rooted local complex.

### 2. Non-tree-edge cycle generation

For every non-tree edge, form the corresponding fundamental cycle.

Define the fundamental cycle of each non-tree edge with respect to the chosen spanning tree.

### 3. Triangle reduction step

Reduce each fundamental cycle to the local triangle scheme.

### 4. Rooted-local generating family

This produces a rooted-local generating family for the local cycle space.

Weakest missing sublemma: the fundamental cycle attached to each non-tree edge lies in the rooted-local generating family.

### 5. Export step

Export the rooted-local generating family to the full local cycle-space generation statement.

## Dependency notes

- `NEWSTEIN_LOCAL_COBOUNDARY_CRITERION.md`
- `NEWSTEIN_ASSEMBLY_THEOREM.md`

## Finish condition

Replace this blueprint by a proof or a proof-complete theorem decomposition for the fundamental cycle-generation sublemma.


Dependency lock: `docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md`.
