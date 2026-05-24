import Chronos.Frontier.R1LongChordCoherenceSufficiency

namespace Chronos
namespace Frontier

/--
A concrete repository-native R1 long-chord witness.

This proves unrestricted native R1 long-chord exclusion is false
without the coherence invariant.
-/
def R1NativeLongChordCounterexampleObject : LongChordNativeObject :=
  {
    leftEndpoint := { id := 0 },
    rightEndpoint := { id := 1 },
    metric := {
      ambientDistance := 10,
      chordLength := 5,
      localityRadius := 2
    }
  }

theorem R1NativeLongChordCounterexampleObject_is_witness :
    LongChordWitness R1NativeLongChordCounterexampleObject := by
  unfold LongChordWitness R1NativeLongChordCounterexampleObject
  decide

theorem R1UnrestrictedNativeLongChordExclusionFalse :
    ¬ NoRepositoryNativeLongChordWitness := by
  intro hNoWitness
  exact hNoWitness
    R1NativeLongChordCounterexampleObject
    R1NativeLongChordCounterexampleObject_is_witness

/--
Restricted replacement for the impossible unrestricted R1 target.

R1 is valid on repository-native coherent carriers, not on all
repository-native long-chord objects.
-/
def R1CoherentLongChordExclusionProofTarget : Prop :=
  RepositoryNativeR1LongChordCoherence → NoRepositoryNativeLongChordWitness

theorem R1CoherentLongChordExclusionProofTarget_proved :
    R1CoherentLongChordExclusionProofTarget := by
  intro hCoherence
  exact repository_native_r1_long_chord_coherence_blocks_witness hCoherence

/--
The weakest native R1 ingredient needed for witness exclusion.
-/
def R1WeakestSufficientNativeIngredientForLongChordExclusion : Prop :=
  RepositoryNativeR1LongChordCoherence

theorem R1WeakestSufficientNativeIngredientForLongChordExclusion_suffices
    (h : R1WeakestSufficientNativeIngredientForLongChordExclusion) :
    NoRepositoryNativeLongChordWitness := by
  exact repository_native_r1_long_chord_coherence_blocks_witness h

/--
Unrestricted R1 remains false/open; coherent R1 is closed.
-/
def R1NativeCounterexampleCoherentRestrictionStatus : String :=
  "UNRESTRICTED_R1_FALSE_COHERENT_R1_CLOSED"

def R1NativeCounterexampleCoherentRestrictionBoundary : String :=
  "Does not prove opaque LongChordExclusionProofTarget, theorem-level R1 promotion, R2, R3, NON_FACTORISATION, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem."

end Frontier
end Chronos
