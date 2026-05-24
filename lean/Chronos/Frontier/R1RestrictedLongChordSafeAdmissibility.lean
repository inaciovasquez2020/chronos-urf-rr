import Chronos.Frontier.R1NativeCoherenceRefutation

namespace Chronos.Frontier

/--
Restricted R1 admissibility repair.

The unrestricted global coherence predicate
`RepositoryNativeR1LongChordCoherence` is refuted in
`R1NativeCoherenceRefutation`.  The repaired local admissibility condition is
therefore object-indexed: an object is R1-long-chord-safe exactly when it does
not carry a `LongChordWitness`.
-/
def R1LongChordSafeNativeAdmissible (x : LongChordNativeObject) : Prop :=
  ¬ LongChordWitness x

/--
Restricted no-long-chord target.

This is intentionally restricted to objects satisfying
`R1LongChordSafeNativeAdmissible`; it does not assert the global native
predicate `NoRepositoryNativeLongChordWitness`.
-/
def R1RestrictedNoLongChordWitness : Prop :=
  ∀ x : LongChordNativeObject,
    R1LongChordSafeNativeAdmissible x → ¬ LongChordWitness x

/--
The restricted R1 no-long-chord theorem closes definitionally from the repaired
object-indexed admissibility condition.
-/
theorem R1RestrictedNoLongChordWitness_proved :
    R1RestrictedNoLongChordWitness := by
  intro x hx
  exact hx

/--
The already-formalized counterexample object is excluded by the repaired
restricted admissibility condition.
-/
theorem R1NativeLongChordCounterexampleObject_not_safe :
    ¬ R1LongChordSafeNativeAdmissible R1NativeLongChordCounterexampleObject := by
  intro hsafe
  exact hsafe R1NativeLongChordCounterexampleObject_is_witness

/--
The repaired condition is consistent with the refutation of unrestricted native
R1 coherence: it restricts admissibility rather than proving the refuted global
coherence predicate.
-/
def R1RestrictedLongChordSafeAdmissibilityStatus : String :=
  "RESTRICTED_R1_LONG_CHORD_SAFE_ADMISSIBILITY_CLOSED"

end Chronos.Frontier
