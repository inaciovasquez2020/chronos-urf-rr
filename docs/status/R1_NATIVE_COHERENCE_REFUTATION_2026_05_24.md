# R1 Native Coherence Refutation — 2026-05-24

Status: `REPOSITORY_NATIVE_R1_LONG_CHORD_COHERENCE_REFUTED`.

This file records the theorem-level resolution of the attempted target
`RepositoryNativeR1LongChordCoherence`.

The positive target is not provable under the current native long-chord
definitions.

Formal chain:

~~~lean
R1CoherentLongChordExclusionProofTarget_proved :
  RepositoryNativeR1LongChordCoherence -> NoRepositoryNativeLongChordWitness

R1UnrestrictedNativeLongChordExclusionFalse :
  ¬ NoRepositoryNativeLongChordWitness
~~~

Therefore:

~~~lean
RepositoryNativeR1LongChordCoherence_refuted :
  ¬ RepositoryNativeR1LongChordCoherence
~~~

The counterexample target is also closed:

~~~lean
R1NativeCoherenceCounterexampleTarget_proved :
  R1NativeCoherenceCounterexampleTarget
~~~

Interpretation:

The current native admissibility package does not force R1 coherence. The
coherence ingredient must be strengthened, renamed, restricted, or supplied as
an external bridge input.

Boundary:

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
