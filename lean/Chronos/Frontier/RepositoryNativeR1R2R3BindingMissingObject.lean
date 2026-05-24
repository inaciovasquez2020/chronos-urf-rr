import Mathlib.Tactic
import Chronos.Frontier.R1R2R3SemanticTheoremProofTargets
import Chronos.Frontier.R1R2R3NonFactorisationPromotionLock

namespace Chronos
namespace Frontier

/--
Missing object required before R1/R2/R3 can be theorem-proved natively.

This is not a proof of R1/R2/R3. It records that the repository currently has
interfaces and promotion locks, but lacks native bindings from the OPEN_INPUTS_REGISTRY
objects to the semantic theorem-proof fields.
-/
structure RepositoryNativeR1R2R3BindingSpec where
  nativeWordSpec : Prop
  nativeEdgeSpec : Prop
  nativeFaceSpec : Prop
  nativeFiberSpec : Prop
  nativeTwoChainSpec : Prop
  nativeQuotientDataSpec : Prop
  r1MatchesOpenInputsRegistry : Prop
  r2MatchesOpenInputsRegistry : Prop
  r3MatchesOpenInputsRegistry : Prop

def RepositoryNativeR1R2R3BindingSupplied
    (S : RepositoryNativeR1R2R3BindingSpec) : Prop :=
  S.nativeWordSpec ∧
  S.nativeEdgeSpec ∧
  S.nativeFaceSpec ∧
  S.nativeFiberSpec ∧
  S.nativeTwoChainSpec ∧
  S.nativeQuotientDataSpec ∧
  S.r1MatchesOpenInputsRegistry ∧
  S.r2MatchesOpenInputsRegistry ∧
  S.r3MatchesOpenInputsRegistry

theorem no_repository_native_R1_R2_R3_theorem_proof_without_binding
    (S : RepositoryNativeR1R2R3BindingSpec)
    (hmissing :
      ¬ S.nativeWordSpec ∨
      ¬ S.nativeEdgeSpec ∨
      ¬ S.nativeFaceSpec ∨
      ¬ S.nativeFiberSpec ∨
      ¬ S.nativeTwoChainSpec ∨
      ¬ S.nativeQuotientDataSpec ∨
      ¬ S.r1MatchesOpenInputsRegistry ∨
      ¬ S.r2MatchesOpenInputsRegistry ∨
      ¬ S.r3MatchesOpenInputsRegistry) :
    ¬ RepositoryNativeR1R2R3BindingSupplied S := by
  intro h
  rcases h with ⟨hWord, hEdge, hFace, hFiber, hTwoChain, hQuotient, hR1, hR2, hR3⟩
  rcases hmissing with hWordMissing | hEdgeMissing | hFaceMissing | hFiberMissing |
    hTwoChainMissing | hQuotientMissing | hR1Missing | hR2Missing | hR3Missing
  · exact hWordMissing hWord
  · exact hEdgeMissing hEdge
  · exact hFaceMissing hFace
  · exact hFiberMissing hFiber
  · exact hTwoChainMissing hTwoChain
  · exact hQuotientMissing hQuotient
  · exact hR1Missing hR1
  · exact hR2Missing hR2
  · exact hR3Missing hR3

end Frontier
end Chronos
