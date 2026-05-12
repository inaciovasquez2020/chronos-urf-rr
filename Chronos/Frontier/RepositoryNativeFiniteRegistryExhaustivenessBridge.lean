import Chronos.Frontier.CurrentUnrestrictedRegSNFStatusLock

/-
Repository-native finite-registry exhaustiveness bridge.

This file proves the finite-generation bridge from the weakest remaining
toolkit admissible registry-exhaustiveness input.

It does not prove RepositoryNativeFiniteRegistryExhaustiveness.
-/

axiom RepositoryNativeFiniteRegistryExhaustiveness :
  ∃ R : Finset ChronosCarrierData,
    ∀ c : ChronosCarrierData,
      FinalCarrierDomain c →
      c ∈ R ∧ RepositoryNativeGenerated c

theorem FinalCarrierGeneratedByFiniteRegistry_from_toolkit :
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
