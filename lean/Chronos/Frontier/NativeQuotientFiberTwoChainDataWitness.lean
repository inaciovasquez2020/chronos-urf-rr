import Mathlib.Tactic
import Chronos.Frontier.NewsteinR1R2R3NativeBindingSpec

namespace Chronos
namespace Frontier

/--
Repository-native quotient/fiber/two-chain data required by the Newstein R1/R2/R3
binding interface.

This is a witness surface for quotient, fiber, and two-chain data only.
It does not construct registry matches or R1/R2/R3 correctness data.
-/
structure NativeQuotientFiberTwoChainData where
  binding : NewsteinR1R2R3NativeBindingSpec
  nativeFiberClassSpecSupplied : binding.nativeFiberClassSpec
  nativeFiberToGlobalQuotientSpecSupplied : binding.nativeFiberToGlobalQuotientSpec
  nativeTwoChainSpecSupplied : binding.nativeTwoChainSpec
  nativeDiameterSpecSupplied : binding.nativeDiameterSpec
  nativeSeparationParameterSpecSupplied : binding.nativeSeparationParameterSpec
  nativeQuotientDataSpecSupplied : binding.nativeQuotientDataSpec
  nativeLocalTypeSpecSupplied : binding.nativeLocalTypeSpec
  nativeCapacityFunctionSpecSupplied : binding.nativeCapacityFunctionSpec

def NativeQuotientFiberTwoChainSupplied
    (Q : NativeQuotientFiberTwoChainData) : Prop :=
  Q.binding.nativeFiberClassSpec ∧
  Q.binding.nativeFiberToGlobalQuotientSpec ∧
  Q.binding.nativeTwoChainSpec ∧
  Q.binding.nativeDiameterSpec ∧
  Q.binding.nativeSeparationParameterSpec ∧
  Q.binding.nativeQuotientDataSpec ∧
  Q.binding.nativeLocalTypeSpec ∧
  Q.binding.nativeCapacityFunctionSpec

theorem native_quotient_fiber_two_chain_supplied
    (Q : NativeQuotientFiberTwoChainData) :
    NativeQuotientFiberTwoChainSupplied Q := by
  exact ⟨
    Q.nativeFiberClassSpecSupplied,
    Q.nativeFiberToGlobalQuotientSpecSupplied,
    Q.nativeTwoChainSpecSupplied,
    Q.nativeDiameterSpecSupplied,
    Q.nativeSeparationParameterSpecSupplied,
    Q.nativeQuotientDataSpecSupplied,
    Q.nativeLocalTypeSpecSupplied,
    Q.nativeCapacityFunctionSpecSupplied
  ⟩

end Frontier
end Chronos
