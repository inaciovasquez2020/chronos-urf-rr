import Chronos.Frontier.NativeLongChordDiameterCapacityIngredients
import Chronos.Frontier.R1R2R3IsolatedTargetsConditionalClosure

namespace Chronos
namespace Frontier

def LongChordExclusionConcreteConfiguration : Type :=
  LongChordNativeObject

def LongChordExclusionConcreteLongChord
    (x : LongChordExclusionConcreteConfiguration) : Prop :=
  LongChordWitness x

def LongChordExclusionConcreteAdmissible
    (x : LongChordExclusionConcreteConfiguration) : Prop :=
  NativeLongChordCoherence x

theorem long_chord_exclusion_concrete_exclusion :
    ∀ C,
      LongChordExclusionConcreteAdmissible C →
        ¬ LongChordExclusionConcreteLongChord C := by
  intro C hAdmissible hLongChord
  exact long_chord_witness_contradiction C hLongChord hAdmissible

def LongChordExclusionConcreteInputSurface :
    LongChordExclusionInputSurface :=
  LongChordExclusionInputSurface.mk
    LongChordExclusionConcreteConfiguration
    LongChordExclusionConcreteLongChord
    LongChordExclusionConcreteAdmissible
    long_chord_exclusion_concrete_exclusion

end Frontier
end Chronos
