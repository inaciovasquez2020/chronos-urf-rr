import Mathlib.Tactic
import Chronos.Frontier.NewsteinR1R2R3NativeBindingSpec

namespace Chronos
namespace Frontier

/--
Simultaneous repository-native binding assembly witness.

This supplies, for one shared native binding specification:
* native geometric specifications,
* native quotient/fiber/two-chain data,
* registry matches,
* R1 correctness,
* R2 correctness,
* R3 correctness.

It does not construct the underlying native mathematical objects beyond the
already declared fields of `NewsteinR1R2R3NativeBindingSpec`.
-/
structure NativeBindingAssemblyData where
  binding : NewsteinR1R2R3NativeBindingSpec
  nativeWTrivSpecSupplied : binding.nativeWTrivSpec
  nativePhi2TrivSpecSupplied : binding.nativePhi2TrivSpec
  nativeBoundaryOperatorSpecSupplied : binding.nativeBoundaryOperatorSpec
  nativeSupportSpecSupplied : binding.nativeSupportSpec
  nativeLongChordSpecSupplied : binding.nativeLongChordSpec
  nativeFiberClassSpecSupplied : binding.nativeFiberClassSpec
  nativeFiberToGlobalQuotientSpecSupplied : binding.nativeFiberToGlobalQuotientSpec
  nativeTwoChainSpecSupplied : binding.nativeTwoChainSpec
  nativeDiameterSpecSupplied : binding.nativeDiameterSpec
  nativeSeparationParameterSpecSupplied : binding.nativeSeparationParameterSpec
  nativeQuotientDataSpecSupplied : binding.nativeQuotientDataSpec
  nativeLocalTypeSpecSupplied : binding.nativeLocalTypeSpec
  nativeCapacityFunctionSpecSupplied : binding.nativeCapacityFunctionSpec
  r1MatchesOpenInputsRegistrySupplied : binding.r1MatchesOpenInputsRegistry
  r2MatchesOpenInputsRegistrySupplied : binding.r2MatchesOpenInputsRegistry
  r3MatchesOpenInputsRegistrySupplied : binding.r3MatchesOpenInputsRegistry

def NativeBindingAssemblySupplied
    (A : NativeBindingAssemblyData) : Prop :=
  NewsteinR1R2R3NativeBindingSupplied A.binding

theorem native_binding_assembly_supplied
    (A : NativeBindingAssemblyData) :
    NativeBindingAssemblySupplied A := by
  dsimp [NativeBindingAssemblySupplied, NewsteinR1R2R3NativeBindingSupplied]
  exact ⟨
    A.nativeWTrivSpecSupplied,
    A.nativePhi2TrivSpecSupplied,
    A.nativeBoundaryOperatorSpecSupplied,
    A.nativeSupportSpecSupplied,
    A.nativeLongChordSpecSupplied,
    A.nativeFiberClassSpecSupplied,
    A.nativeFiberToGlobalQuotientSpecSupplied,
    A.nativeTwoChainSpecSupplied,
    A.nativeDiameterSpecSupplied,
    A.nativeSeparationParameterSpecSupplied,
    A.nativeQuotientDataSpecSupplied,
    A.nativeLocalTypeSpecSupplied,
    A.nativeCapacityFunctionSpecSupplied,
    A.r1MatchesOpenInputsRegistrySupplied,
    A.r2MatchesOpenInputsRegistrySupplied,
    A.r3MatchesOpenInputsRegistrySupplied,
    A.binding.r1Correct,
    A.binding.r2Correct,
    A.binding.r3Correct
  ⟩

end Frontier
end Chronos
