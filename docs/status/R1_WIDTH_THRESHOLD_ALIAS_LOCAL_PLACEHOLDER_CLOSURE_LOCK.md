# R1 Width-Threshold Alias Local Placeholder Closure Lock

Status: `LOCAL_PLACEHOLDER_ALIAS_PRECONDITIONS_CLOSED_ONLY`

Artifact:

- `artifacts/chronos/r1_width_threshold_alias_local_placeholder_closure_lock_2026_06_20.json`

Verifier:

- `tools/verify_r1_width_threshold_alias_local_placeholder_closure_lock.py`

The lock records that the currently surfaced R1 width-threshold alias preconditions are closed only over the repository's local placeholder surfaces:

1. domain identity;
2. obstruction measure identity;
3. same local obstruction measure bounds.

The third item is supplied by:

- `artifacts/chronos/r1_obstruction_measure_bound_to_width_threshold_alias_bridge_2026_06_20.json`
- `lean/Chronos/Frontier/R1ObstructionMeasureBoundSurface.lean`

Boundary:

`BOUNDARY := ¬ unrestricted_Chronos_RR`

This status document does not assert native `cross(gamma,L)` semantics, native `SkeletonDistance_I(endpoints(c))` semantics, endpoint extraction semantics, native obstruction-measure semantics, native `w(P,L)` semantics, native `LongChordThreshold(I)` semantics, unconditional `w(P,L) = LongChordThreshold(I)`, native R1/R2/R3, or unrestricted Chronos-RR.
