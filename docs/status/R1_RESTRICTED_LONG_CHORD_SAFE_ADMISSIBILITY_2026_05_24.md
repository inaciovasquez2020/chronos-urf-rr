# R1 Restricted Long-Chord-Safe Admissibility — 2026-05-24

Status: `RESTRICTED_R1_LONG_CHORD_SAFE_ADMISSIBILITY_CLOSED`.

The unrestricted predicate `RepositoryNativeR1LongChordCoherence` has been
refuted under the current native long-chord definitions. This file introduces
the repaired restricted condition:

~~~lean
R1LongChordSafeNativeAdmissible x := ¬ LongChordWitness x
~~~

The restricted bridge is:

~~~lean
R1RestrictedNoLongChordWitness :=
  ∀ x : LongChordNativeObject,
    R1LongChordSafeNativeAdmissible x → ¬ LongChordWitness x
~~~

Closed theorem:

~~~lean
R1RestrictedNoLongChordWitness_proved :
  R1RestrictedNoLongChordWitness
~~~

The known counterexample is excluded by the repaired condition:

~~~lean
R1NativeLongChordCounterexampleObject_not_safe :
  ¬ R1LongChordSafeNativeAdmissible R1NativeLongChordCounterexampleObject
~~~

Interpretation:

This does not resurrect the refuted global coherence predicate. It creates the
correct restricted admissibility gate for R1 long-chord safety.

Boundary:

- does not prove RepositoryNativeR1LongChordCoherence
- does not prove NoRepositoryNativeLongChordWitness
- does not prove opaque LongChordExclusionProofTarget
- does not prove theorem-level unrestricted R1 promotion
- does not prove R2
- does not prove R3
- does not prove NON_FACTORISATION
- does not prove Chronos-RR
- does not prove H4.1/FGL
- does not prove P vs NP
- does not prove any Clay problem
