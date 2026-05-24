# R1 Native Coherence Promotion Target — 2026-05-24

Status: `OPEN_PROMOTION_TARGET_ONLY`.

This file records the exact remaining R1 native-promotion problem after the
unrestricted native R1 long-chord exclusion was refuted.

Accepted prior state:

- `R1UnrestrictedNativeLongChordExclusionFalse`
- `R1CoherentLongChordExclusionProofTarget_proved`
- `R1WeakestSufficientNativeIngredientForLongChordExclusion_suffices`

The remaining target is:

~~~lean
NativeAdmissibilityPackage -> RepositoryNativeR1LongChordCoherence
~~~

The counterexample target is:

~~~lean
NativeAdmissibilityPackage ∧ ¬ RepositoryNativeR1LongChordCoherence
~~~

Boundary:

- does not prove NativeAdmissibilityPackage -> RepositoryNativeR1LongChordCoherence
- does not prove RepositoryNativeR1LongChordCoherence
- does not prove NoRepositoryNativeLongChordWitness
- does not prove opaque LongChordExclusionProofTarget
- does not prove theorem-level R1 promotion
- does not prove R2
- does not prove R3
- does not prove NON_FACTORISATION
- does not prove Chronos-RR
- does not prove H4.1/FGL
- does not prove P vs NP
- does not prove any Clay problem

This is an R1 coherence-promotion target only.
