import Mathlib.Tactic
import Chronos.Frontier.NewsteinR1R2R3NativeBindingSpec

namespace Chronos
namespace Frontier

/--
Repository-native geometric specification data required by the Newstein R1/R2/R3
binding interface.

This is a witness surface for the geometric specification layer only.
It does not construct quotient, fiber, two-chain, registry, or R1/R2/R3
correctness data.
-/
structure NativeGeometricSpecificationData where
  binding : NewsteinR1R2R3NativeBindingSpec
  nativeWTrivSpecSupplied : binding.nativeWTrivSpec
  nativePhi2TrivSpecSupplied : binding.nativePhi2TrivSpec
  nativeBoundaryOperatorSpecSupplied : binding.nativeBoundaryOperatorSpec
  nativeSupportSpecSupplied : binding.nativeSupportSpec
  nativeLongChordSpecSupplied : binding.nativeLongChordSpec

def NativeGeometricSpecificationSupplied
    (G : NativeGeometricSpecificationData) : Prop :=
  G.binding.nativeWTrivSpec ∧
  G.binding.nativePhi2TrivSpec ∧
  G.binding.nativeBoundaryOperatorSpec ∧
  G.binding.nativeSupportSpec ∧
  G.binding.nativeLongChordSpec

theorem native_geometric_specification_supplied
    (G : NativeGeometricSpecificationData) :
    NativeGeometricSpecificationSupplied G := by
  exact ⟨
    G.nativeWTrivSpecSupplied,
    G.nativePhi2TrivSpecSupplied,
    G.nativeBoundaryOperatorSpecSupplied,
    G.nativeSupportSpecSupplied,
    G.nativeLongChordSpecSupplied
  ⟩

end Frontier
end Chronos
