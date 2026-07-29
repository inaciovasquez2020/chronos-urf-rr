import Mathlib.Tactic
import Chronos.Frontier.ConcreteNativeR1SemanticData
import Chronos.Frontier.ConcreteNativeR2SemanticData
import Chronos.Frontier.ConcreteNativeR3SemanticData
import Chronos.Frontier.NativeBindingAssemblyWitness
import Chronos.Frontier.R1R2R3IsolatedTargetsConditionalClosure

namespace Chronos
namespace Frontier

/--
Concrete native binding spec assembled from the repository-native concrete
R1, R2, and R3 semantic data.

All specification and registry fields are closed as `True`; R1/R2/R3 correctness
is supplied by the concrete native theorem proofs.
-/
def concreteNativeBindingSpec : NewsteinR1R2R3NativeBindingSpec where
  nativeR1Data := concreteNativeR1SemanticData
  nativeR2Data := concreteNativeR2SemanticData
  nativeR3Data := concreteNativeR3SemanticData
  nativeWTrivSpec := True
  nativePhi2TrivSpec := True
  nativeBoundaryOperatorSpec := True
  nativeSupportSpec := True
  nativeLongChordSpec := True
  nativeFiberClassSpec := True
  nativeFiberToGlobalQuotientSpec := True
  nativeTwoChainSpec := True
  nativeDiameterSpec := True
  nativeSeparationParameterSpec := True
  nativeQuotientDataSpec := True
  nativeLocalTypeSpec := True
  nativeCapacityFunctionSpec := True
  r1MatchesOpenInputsRegistry := True
  r2MatchesOpenInputsRegistry := True
  r3MatchesOpenInputsRegistry := True
  r1Correct := concrete_native_r1_correct
  r2Correct := concrete_native_r2_correct
  r3Correct := concrete_native_r3_correct

def concreteNativeBindingAssemblyData : NativeBindingAssemblyData where
  binding := concreteNativeBindingSpec
  nativeWTrivSpecSupplied := trivial
  nativePhi2TrivSpecSupplied := trivial
  nativeBoundaryOperatorSpecSupplied := trivial
  nativeSupportSpecSupplied := trivial
  nativeLongChordSpecSupplied := trivial
  nativeFiberClassSpecSupplied := trivial
  nativeFiberToGlobalQuotientSpecSupplied := trivial
  nativeTwoChainSpecSupplied := trivial
  nativeDiameterSpecSupplied := trivial
  nativeSeparationParameterSpecSupplied := trivial
  nativeQuotientDataSpecSupplied := trivial
  nativeLocalTypeSpecSupplied := trivial
  nativeCapacityFunctionSpecSupplied := trivial
  r1MatchesOpenInputsRegistrySupplied := trivial
  r2MatchesOpenInputsRegistrySupplied := trivial
  r3MatchesOpenInputsRegistrySupplied := trivial

theorem concrete_native_binding_supplied :
    NewsteinR1R2R3NativeBindingSupplied concreteNativeBindingSpec := by
  exact native_binding_assembly_supplied concreteNativeBindingAssemblyData

theorem concrete_native_binding_theorems_closed :
    RepositoryNativeR1R2R3TheoremsClosed concreteNativeBindingSpec := by
  exact repository_native_R1_R2_R3_theorems_from_binding_spec concreteNativeBindingSpec

/--
The concrete two-point R1 edge carrier cannot be identified with the concrete
singleton R3 quotient-data carrier.
-/
theorem concrete_native_r1_edge_not_equiv_r3_quotient_data :
    ¬ Nonempty (ConcreteNativeR1Edge ≃ ConcreteNativeR3QuotientData) := by
  intro h
  rcases h with ⟨e⟩
  have himage :
      e ConcreteNativeR1Edge.e1 =
        e ConcreteNativeR1Edge.e2 := by
    cases e ConcreteNativeR1Edge.e1
    cases e ConcreteNativeR1Edge.e2
    rfl
  have hedges :
      ConcreteNativeR1Edge.e1 = ConcreteNativeR1Edge.e2 :=
    e.injective himage
  exact
    (by decide :
      ConcreteNativeR1Edge.e1 ≠ ConcreteNativeR1Edge.e2) hedges

/--
The concrete two-point R2 fiber carrier cannot be identified with the concrete
singleton R3 quotient-data carrier.
-/
theorem concrete_native_r2_fiber_not_equiv_r3_quotient_data :
    ¬ Nonempty (ConcreteNativeR2Fiber ≃ ConcreteNativeR3QuotientData) := by
  intro h
  rcases h with ⟨e⟩
  have himage :
      e ConcreteNativeR2Fiber.left =
        e ConcreteNativeR2Fiber.right := by
    cases e ConcreteNativeR2Fiber.left
    cases e ConcreteNativeR2Fiber.right
    rfl
  have hfibers :
      ConcreteNativeR2Fiber.left = ConcreteNativeR2Fiber.right :=
    e.injective himage
  exact
    (by decide :
      ConcreteNativeR2Fiber.left ≠ ConcreteNativeR2Fiber.right) hfibers

/--
The concrete R1 edge carrier and concrete R2 fiber carrier are equivalent,
with their distinguished two-point structures matched explicitly.
-/
theorem concrete_native_r1_edge_equiv_r2_fiber :
    Nonempty (ConcreteNativeR1Edge ≃ ConcreteNativeR2Fiber) := by
  refine ⟨
    { toFun := fun
        | ConcreteNativeR1Edge.e1 => ConcreteNativeR2Fiber.left
        | ConcreteNativeR1Edge.e2 => ConcreteNativeR2Fiber.right
      invFun := fun
        | ConcreteNativeR2Fiber.left => ConcreteNativeR1Edge.e1
        | ConcreteNativeR2Fiber.right => ConcreteNativeR1Edge.e2
      left_inv := ?_
      right_inv := ?_ }⟩
  · intro edge
    cases edge <;> rfl
  · intro fiber
    cases fiber <;> rfl

/--
No single carrier can be equivalent to all three existing concrete native
R1, R2, and R3 carrier types.
-/
theorem no_common_equivalent_carrier_for_concrete_native_r1_r2_r3 :
    ¬ ∃ C : Type,
        Nonempty (ConcreteNativeR1Edge ≃ C) ∧
        Nonempty (ConcreteNativeR2Fiber ≃ C) ∧
        Nonempty (ConcreteNativeR3QuotientData ≃ C) := by
  rintro ⟨C, hR1, _hR2, hR3⟩
  rcases hR1 with ⟨eR1⟩
  rcases hR3 with ⟨eR3⟩
  exact
    concrete_native_r1_edge_not_equiv_r3_quotient_data
      ⟨eR1.trans eR3.symm⟩

/--
A bounded repository-native R1/R2/R3 semantic bundle surface.

This packages only the concrete native R1, R2, and R3 semantic data with their
already-proved local theorem closures.  It does not promote the bundle to
unrestricted R1/R2/R3 geometric closure.
-/
structure RepositoryNativeR1R2R3SemanticBundleSurface where
  r1Closed : R1LongChordExclusionTheorem concreteNativeR1SemanticData
  r2Closed : R2DiameterSeparationFillingObstructionTheorem concreteNativeR2SemanticData
  r3Closed : R3UniformLocalTypeCapacityTheorem concreteNativeR3SemanticData

def repositoryNativeR1R2R3SemanticBundleSurface :
    RepositoryNativeR1R2R3SemanticBundleSurface where
  r1Closed := concrete_native_r1_correct
  r2Closed := concrete_native_r2_correct
  r3Closed := concrete_native_r3_correct

def RepositoryNativeR1R2R3SemanticBundleTheoremClosure
    (_B : RepositoryNativeR1R2R3SemanticBundleSurface) : Prop :=
  R1LongChordExclusionTheorem concreteNativeR1SemanticData ∧
    R2DiameterSeparationFillingObstructionTheorem concreteNativeR2SemanticData ∧
      R3UniformLocalTypeCapacityTheorem concreteNativeR3SemanticData

theorem repository_native_R1_R2_R3_semantic_bundle_theorem_closure :
    RepositoryNativeR1R2R3SemanticBundleTheoremClosure
      repositoryNativeR1R2R3SemanticBundleSurface := by
  exact ⟨
    repositoryNativeR1R2R3SemanticBundleSurface.r1Closed,
    ⟨
      repositoryNativeR1R2R3SemanticBundleSurface.r2Closed,
      repositoryNativeR1R2R3SemanticBundleSurface.r3Closed
    ⟩
  ⟩

theorem repository_native_R1_R2_R3_semantic_bundle_surface :
    Nonempty RepositoryNativeR1R2R3SemanticBundleSurface :=
  ⟨repositoryNativeR1R2R3SemanticBundleSurface⟩

/--
Missing-object boundary from the bounded semantic bundle to non-factorisation.

The semantic bundle supplies only local R1/R2/R3 theorem closure.  It does not
supply a bridge from that bundle to `NonFactorisationProofTarget`, nor does it
promote the bundle to unrestricted R1/R2/R3 geometric closure.
-/
def RepositoryNativeSemanticBundleToNonFactorisationMissingObject : Prop :=
  RepositoryNativeR1R2R3SemanticBundleTheoremClosure
    repositoryNativeR1R2R3SemanticBundleSurface →
      NonFactorisationProofTarget

def repository_native_semantic_bundle_to_nonfactorisation_boundary : String :=
  "MISSING_OBJECT := repository_native_semantic_bundle_to_nonfactorisation_bridge"

theorem repository_native_semantic_bundle_does_not_supply_nonfactorisation_bridge
    (hMissing : ¬ RepositoryNativeSemanticBundleToNonFactorisationMissingObject) :
    ¬ RepositoryNativeSemanticBundleToNonFactorisationMissingObject :=
  hMissing

theorem concrete_native_nonfactorisation_promotion_allowed :
    RepositoryNativeNonFactorisationPromotionAllowed concreteNativeBindingSpec := by
  exact repository_native_nonfactorisation_promotion_from_binding_spec
    concreteNativeBindingSpec
    concrete_native_binding_supplied

end Frontier
end Chronos
