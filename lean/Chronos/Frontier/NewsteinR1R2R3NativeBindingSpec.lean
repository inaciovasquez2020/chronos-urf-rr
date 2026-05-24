import Mathlib.Tactic
import Chronos.Frontier.R1R2R3SemanticTheoremProofTargets
import Chronos.Frontier.R1R2R3NonFactorisationPromotionLock

namespace Chronos
namespace Frontier

/--
Repository-native Newstein R1/R2/R3 binding specification.

This is a specification object only.  It records the exact native objects and
correctness obligations required before the conditional R1/R2/R3 theorem-proof
route can be promoted.

It does not construct the native objects.
It does not prove R1, R2, R3, NON_FACTORISATION, Chronos-RR, or H4.1/FGL.
-/
structure RepositoryNativeR1R2R3BindingSpec where
  nativeR1Data : R1SemanticData
  nativeR2Data : R2SemanticData
  nativeR3Data : R3SemanticData

  nativeWTrivSpec : Prop
  nativePhi2TrivSpec : Prop
  nativeBoundaryOperatorSpec : Prop
  nativeSupportSpec : Prop
  nativeLongChordSpec : Prop

  nativeFiberClassSpec : Prop
  nativeFiberToGlobalQuotientSpec : Prop
  nativeTwoChainSpec : Prop
  nativeDiameterSpec : Prop
  nativeSeparationParameterSpec : Prop

  nativeQuotientDataSpec : Prop
  nativeLocalTypeSpec : Prop
  nativeCapacityFunctionSpec : Prop

  r1MatchesOpenInputsRegistry : Prop
  r2MatchesOpenInputsRegistry : Prop
  r3MatchesOpenInputsRegistry : Prop

  r1Correct : R1LongChordExclusionTheorem nativeR1Data
  r2Correct : R2DiameterSeparationFillingObstructionTheorem nativeR2Data
  r3Correct : R3UniformLocalTypeCapacityTheorem nativeR3Data

/-- The native binding is supplied exactly when all registry-matching specs are present. -/
def RepositoryNativeR1R2R3BindingSupplied
    (S : RepositoryNativeR1R2R3BindingSpec) : Prop :=
  S.nativeWTrivSpec ∧
  S.nativePhi2TrivSpec ∧
  S.nativeBoundaryOperatorSpec ∧
  S.nativeSupportSpec ∧
  S.nativeLongChordSpec ∧
  S.nativeFiberClassSpec ∧
  S.nativeFiberToGlobalQuotientSpec ∧
  S.nativeTwoChainSpec ∧
  S.nativeDiameterSpec ∧
  S.nativeSeparationParameterSpec ∧
  S.nativeQuotientDataSpec ∧
  S.nativeLocalTypeSpec ∧
  S.nativeCapacityFunctionSpec ∧
  S.r1MatchesOpenInputsRegistry ∧
  S.r2MatchesOpenInputsRegistry ∧
  S.r3MatchesOpenInputsRegistry

/--
If a repository-native binding spec is supplied, then the R1/R2/R3 semantic theorem
targets are closed for the native data.
-/
def RepositoryNativeR1R2R3TheoremsClosed
    (S : RepositoryNativeR1R2R3BindingSpec) : Prop :=
  R1LongChordExclusionTheorem S.nativeR1Data ∧
  R2DiameterSeparationFillingObstructionTheorem S.nativeR2Data ∧
  R3UniformLocalTypeCapacityTheorem S.nativeR3Data

theorem repository_native_R1_R2_R3_theorems_from_binding_spec
    (S : RepositoryNativeR1R2R3BindingSpec) :
    RepositoryNativeR1R2R3TheoremsClosed S := by
  exact ⟨S.r1Correct, S.r2Correct, S.r3Correct⟩

/--
Native non-factorisation promotion is allowed only from a supplied native binding
and the native R1/R2/R3 theorem closures.
-/
def RepositoryNativeNonFactorisationPromotionAllowed
    (S : RepositoryNativeR1R2R3BindingSpec) : Prop :=
  RepositoryNativeR1R2R3BindingSupplied S ∧
  RepositoryNativeR1R2R3TheoremsClosed S

theorem repository_native_nonfactorisation_promotion_from_binding_spec
    (S : RepositoryNativeR1R2R3BindingSpec)
    (hSupplied : RepositoryNativeR1R2R3BindingSupplied S) :
    RepositoryNativeNonFactorisationPromotionAllowed S := by
  exact ⟨hSupplied, repository_native_R1_R2_R3_theorems_from_binding_spec S⟩

/--
Chronos-RR promotion is still blocked unless the repository-native binding is supplied.
-/
def RepositoryNativeChronosRRPromotionAllowed
    (S : RepositoryNativeR1R2R3BindingSpec) : Prop :=
  RepositoryNativeNonFactorisationPromotionAllowed S

/--
H4.1/FGL promotion is still blocked unless the repository-native binding is supplied.
-/
def RepositoryNativeH41FGLPromotionAllowed
    (S : RepositoryNativeR1R2R3BindingSpec) : Prop :=
  RepositoryNativeNonFactorisationPromotionAllowed S

theorem no_repository_native_promotion_without_binding_supplied
    (S : RepositoryNativeR1R2R3BindingSpec)
    (hMissing : ¬ RepositoryNativeR1R2R3BindingSupplied S) :
    ¬ RepositoryNativeNonFactorisationPromotionAllowed S := by
  intro hAllowed
  exact hMissing hAllowed.1

theorem no_repository_native_chronos_rr_promotion_without_binding_supplied
    (S : RepositoryNativeR1R2R3BindingSpec)
    (hMissing : ¬ RepositoryNativeR1R2R3BindingSupplied S) :
    ¬ RepositoryNativeChronosRRPromotionAllowed S := by
  exact no_repository_native_promotion_without_binding_supplied S hMissing

theorem no_repository_native_h41_fgl_promotion_without_binding_supplied
    (S : RepositoryNativeR1R2R3BindingSpec)
    (hMissing : ¬ RepositoryNativeR1R2R3BindingSupplied S) :
    ¬ RepositoryNativeH41FGLPromotionAllowed S := by
  exact no_repository_native_promotion_without_binding_supplied S hMissing

end Frontier
end Chronos
