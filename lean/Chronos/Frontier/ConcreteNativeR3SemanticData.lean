import Mathlib.Tactic
import Chronos.Frontier.NewsteinR1R2R3NativeBindingSpec

namespace Chronos
namespace Frontier

/--
Concrete repository-native R3 quotient-data object.

The unique quotient datum has dimension `0` and factors through the bounded
local type by construction.
-/
inductive ConcreteNativeR3QuotientData where
  | unit
deriving DecidableEq

def concreteNativeR3Dim (_quotient : ConcreteNativeR3QuotientData) : Nat := 0

def concreteNativeR3FactorsThroughBoundedLocalType
    (_quotient : ConcreteNativeR3QuotientData) : Prop :=
  True

/--
Concrete repository-native R3 semantic data.

This realizes explicit `QuotientData`, `dim`, and
`FactorsThroughBoundedLocalType` data inside the existing `R3SemanticData`
interface.
-/
def concreteNativeR3SemanticData : R3SemanticData where
  QuotientData := ConcreteNativeR3QuotientData
  C := 0
  dim := concreteNativeR3Dim
  FactorsThroughBoundedLocalType := concreteNativeR3FactorsThroughBoundedLocalType

theorem concrete_native_r3_correct :
    R3UniformLocalTypeCapacityTheorem concreteNativeR3SemanticData := by
  intro quotient hfactor
  cases quotient
  simp [concreteNativeR3SemanticData, concreteNativeR3Dim]

/--
A binding spec is connected to the concrete native R3 construction when its R3
semantic data is exactly the concrete native R3 semantic data.
-/
def NewsteinBindingUsesConcreteNativeR3
    (S : NewsteinR1R2R3NativeBindingSpec) : Prop :=
  S.nativeR3Data = concreteNativeR3SemanticData

theorem newstein_binding_concrete_native_r3_correct
    (S : NewsteinR1R2R3NativeBindingSpec)
    (h : NewsteinBindingUsesConcreteNativeR3 S) :
    R3UniformLocalTypeCapacityTheorem S.nativeR3Data := by
  rw [h]
  exact concrete_native_r3_correct

end Frontier
end Chronos
