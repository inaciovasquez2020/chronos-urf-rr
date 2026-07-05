import Chronos.Frontier.NativeLongChordDiameterCapacityIngredients
import Chronos.Frontier.R1R2R3IsolatedTargetsConditionalClosure

namespace Chronos
namespace Frontier

def DiameterSeparationFillingConcreteConfiguration : Type :=
  DiameterFillingNativeObject

def DiameterSeparationFillingConcreteDiameterSeparated
    (x : DiameterSeparationFillingConcreteConfiguration) : Prop :=
  DiameterFillingCompatibility x

def DiameterSeparationFillingConcreteFillable
    (x : DiameterSeparationFillingConcreteConfiguration) : Prop :=
  x.targetDiameter + x.fillingCost < x.separationFloor

theorem diameter_separation_filling_concrete_obstruction :
    ∀ C,
      DiameterSeparationFillingConcreteDiameterSeparated C →
        ¬ DiameterSeparationFillingConcreteFillable C := by
  intro C hSeparated hFillable
  exact Nat.not_lt_of_ge
    (monotone_separation_lower_bound C hSeparated)
    hFillable

def DiameterSeparationFillingConcreteInputSurface :
    DiameterSeparationFillingObstructionInputSurface :=
  DiameterSeparationFillingObstructionInputSurface.mk
    DiameterSeparationFillingConcreteConfiguration
    DiameterSeparationFillingConcreteDiameterSeparated
    DiameterSeparationFillingConcreteFillable
    diameter_separation_filling_concrete_obstruction

end Frontier
end Chronos
