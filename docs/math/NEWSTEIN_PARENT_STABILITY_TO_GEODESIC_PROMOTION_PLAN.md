# Newstein Parent-Stability-to-Geodesic Promotion Plan

## Status
OPEN

## Goal
Package the full promotion chain from the atomic parent step to geodesic interpolation closure.

## Dependency chain
1. NEWSTEIN_PARENT_DEPTH_DECREMENT_SUBLEMMA.md
2. NEWSTEIN_ROOTED_DISTANCE_MONOTONICITY_SUBLEMMA.md
3. NEWSTEIN_ONE_STEP_PARENT_STABILITY_PREDICATE.md
4. NEWSTEIN_PARENT_ITERATION_CLOSURE_SUBLEMMA.md
5. NEWSTEIN_ANCESTOR_DESCENT_CLOSURE_SUBLEMMA.md
6. NEWSTEIN_LCA_INTERPOLATION_CLOSURE_SUBLEMMA.md
7. NEWSTEIN_GEODESIC_INTERPOLATION_CLOSURE_SUBLEMMA.md

## Promotion rule
If the first two objects are proved, one-step parent stability is discharged.
If one-step parent stability is discharged, the remaining five objects reduce by previously locked blueprints.

## Weakest remaining theorem in this block
Newstein Parent Depth Decrement Sublemma.
