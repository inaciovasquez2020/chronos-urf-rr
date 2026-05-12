import Chronos.Frontier.RepositoryNativeFiniteRegistryExhaustivenessFromFintype

/-
Projection of the generation obligation.

This proves the currently isolated generation obligation from the existing
repository-native finite-registry exhaustiveness axiom.

It does not prove RepositoryNativeFiniteRegistryExhaustiveness.
-/

theorem FinalCarrierDomain_repository_native_generated_from_finite_registry_exhaustiveness :
    ∀ c : ChronosCarrierData,
      FinalCarrierDomain c →
      RepositoryNativeGenerated c := by
  intro c hc
  rcases RepositoryNativeFiniteRegistryExhaustiveness with ⟨R, hR⟩
  exact (hR c hc).2

noncomputable theorem RepositoryNativeFiniteRegistryExhaustiveness_from_projected_generation
    [DecidableEq ChronosCarrierData] :
    ∃ R : Finset ChronosCarrierData,
      ∀ c : ChronosCarrierData,
        FinalCarrierDomain c →
        c ∈ R ∧ RepositoryNativeGenerated c := by
  letI := FinalCarrierDomain_fintype
  exact RepositoryNativeFiniteRegistryExhaustiveness_from_fintype
    FinalCarrierDomain_repository_native_generated_from_finite_registry_exhaustiveness
