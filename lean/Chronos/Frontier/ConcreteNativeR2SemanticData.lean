import Mathlib.Tactic
import Chronos.Frontier.NewsteinR1R2R3NativeBindingSpec

namespace Chronos
namespace Frontier

/--
Concrete repository-native R2 fiber object.

This is the minimal closed native object currently available in the repository:
a two-point fiber with endpoints separated by construction.
-/
inductive ConcreteNativeR2Fiber where
  | left
  | right
deriving DecidableEq

/--
Concrete repository-native R2 two-chain object.

The unique chain has diameter `1`.
-/
inductive ConcreteNativeR2TwoChain where
  | bridge
deriving DecidableEq

def concreteNativeR2Diameter : ConcreteNativeR2TwoChain → Nat
  | ConcreteNativeR2TwoChain.bridge => 1

def concreteNativeR2BoundaryBetween
    (_chain : ConcreteNativeR2TwoChain)
    (u v : ConcreteNativeR2Fiber) : Prop :=
  u ≠ v

/--
Concrete repository-native R2 semantic data.

This realizes explicit `Fiber`, `TwoChain`, `BoundaryBetween`, and `diameter`
data inside the existing `R2SemanticData` interface.
-/
def concreteNativeR2SemanticData : R2SemanticData where
  Fiber := ConcreteNativeR2Fiber
  TwoChain := ConcreteNativeR2TwoChain
  L := 0
  diameter := concreteNativeR2Diameter
  BoundaryBetween := concreteNativeR2BoundaryBetween

theorem concrete_native_r2_correct :
    R2DiameterSeparationFillingObstructionTheorem concreteNativeR2SemanticData := by
  intro chain u v huv hboundary
  cases chain
  simp [concreteNativeR2SemanticData, concreteNativeR2Diameter]

/--
A binding spec is connected to the concrete native R2 construction when its R2
semantic data is exactly the concrete native R2 semantic data.
-/
def NewsteinBindingUsesConcreteNativeR2
    (S : NewsteinR1R2R3NativeBindingSpec) : Prop :=
  S.nativeR2Data = concreteNativeR2SemanticData

theorem newstein_binding_concrete_native_r2_correct
    (S : NewsteinR1R2R3NativeBindingSpec)
    (h : NewsteinBindingUsesConcreteNativeR2 S) :
    R2DiameterSeparationFillingObstructionTheorem S.nativeR2Data := by
  rw [h]
  exact concrete_native_r2_correct

end Frontier
end Chronos
