import Chronos.Frontier.NativeLongChordDiameterCapacityIngredients
import Chronos.Frontier.R1R2R3IsolatedTargetsConditionalClosure

namespace Chronos
namespace Frontier

def UniformLocalTypeCapacityConcreteConfiguration : Type :=
  LocalTypeCapacityNativeObject

def UniformLocalTypeCapacityConcreteLocalType
    (x : UniformLocalTypeCapacityConcreteConfiguration) : Type :=
  Fin x.localTypeCount

def UniformLocalTypeCapacityConcreteCapacityBound : Nat :=
  ExplicitLocalTypeCapacityC

theorem uniform_local_type_capacity_concrete_bounded :
    ∀ C,
      Nonempty (UniformLocalTypeCapacityConcreteLocalType C) →
        UniformLocalTypeCapacityConcreteCapacityBound ≥ 0 := by
  intro C hLocalType
  exact Nat.zero_le UniformLocalTypeCapacityConcreteCapacityBound

def UniformLocalTypeCapacityConcreteInputSurface :
    UniformLocalTypeCapacityInputSurface :=
  UniformLocalTypeCapacityInputSurface.mk
    UniformLocalTypeCapacityConcreteConfiguration
    UniformLocalTypeCapacityConcreteLocalType
    UniformLocalTypeCapacityConcreteCapacityBound
    uniform_local_type_capacity_concrete_bounded

end Frontier
end Chronos
