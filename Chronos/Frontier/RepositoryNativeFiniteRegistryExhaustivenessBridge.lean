import Chronos.Frontier.CurrentUnrestrictedRegSNFStatusLock
import Chronos.Frontier.PositiveArityRepositoryNativeCoverage

/-
Repository-native finite-registry exhaustiveness bridge.

This file proves the finite-generation bridge from the weakest remaining
toolkit admissible registry-exhaustiveness input.

It does not prove RepositoryNativeFiniteRegistryExhaustiveness.
-/

noncomputable def RepositoryNativeFiniteRegistryExhaustiveness
    [DecidableEq ChronosCarrierData]
    [Fintype { c : ChronosCarrierData // FinalCarrierDomain c }] :
  ∃ R : Finset ChronosCarrierData,
    ∀ c : ChronosCarrierData,
      FinalCarrierDomain c →
      c ∈ R ∧ RepositoryNativeGenerated c := by
  refine ⟨Finset.univ.image Subtype.val, fun c hc => ⟨?_, ?_⟩⟩
  · exact Finset.mem_image.mpr ⟨⟨c, hc⟩, Finset.mem_univ _, rfl⟩
  · exact positive_arity_repository_native_image_covers c (by
      simpa [FinalCarrierDomain] using hc)

noncomputable theorem FinalCarrierGeneratedByFiniteRegistry_from_toolkit
    [DecidableEq ChronosCarrierData]
    [Fintype { c : ChronosCarrierData // FinalCarrierDomain c }] :
    ∃ R : Finset ChronosCarrierData,
      ∀ c : ChronosCarrierData,
        FinalCarrierDomain c →
        RepositoryNativeGenerated c ∧ c ∈ R := by
  rcases RepositoryNativeFiniteRegistryExhaustiveness with ⟨R, hR⟩
  refine ⟨R, ?_⟩
  intro c hc
  exact ⟨(hR c hc).2, (hR c hc).1⟩

theorem UniversalFiberEntropyGap_from_toolkit_registry
    (hNF : FinalCarrierDomainNormalFormStratumBound) :
    UniversalFiberEntropyGap := by
  exact UniversalFiberEntropyGap_from_finite_registry_generation hNF
