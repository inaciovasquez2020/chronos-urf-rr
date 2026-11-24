# R1 Width-Threshold Alias Local Placeholder Closure Lock

Status: `LOCAL_PLACEHOLDER_ALIAS_PRECONDITIONS_PARTIAL_ONLY`

Artifact:

- `artifacts/chronos/r1_width_threshold_alias_local_placeholder_closure_lock_2026_06_20.json`

Verifier:

- `tools/verify_r1_width_threshold_alias_local_placeholder_closure_lock.py`

The lock records two locally discharged placeholder-only preconditions:

1. obstruction measure identity;
2. same local obstruction measure bounds.

**The domain identity remains OPEN.** The Lean theorem provides pointwise
equality for `R1NativeCandidateChord G`, whose subtype already carries an
adjacency witness. `MarkedBoundaryChord` is still the placeholder `True`.
This is not an unrestricted identification of native chord domains.

The second item is supplied by:

- `artifacts/chronos/r1_obstruction_measure_bound_to_width_threshold_alias_bridge_2026_06_20.json`
- `lean/Chronos/Frontier/R1ObstructionMeasureBoundSurface.lean`

Boundary:

`BOUNDARY := ¬ unrestricted_Chronos_RR`

This status document does not assert native `cross(gamma,L)` semantics, native `SkeletonDistance_I(endpoints(c))` semantics, endpoint extraction semantics, native obstruction-measure semantics, native `w(P,L)` semantics, native `LongChordThreshold(I)` semantics, unconditional `w(P,L) = LongChordThreshold(I)`, native R1/R2/R3, or unrestricted Chronos-RR.
