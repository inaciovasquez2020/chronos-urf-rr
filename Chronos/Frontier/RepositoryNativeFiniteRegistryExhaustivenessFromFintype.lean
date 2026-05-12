import Chronos.Frontier.RepositoryNativeFiniteRegistryExhaustivenessBridge

/-
Fintype reduction for repository-native finite-registry exhaustiveness.

This proves RepositoryNativeFiniteRegistryExhaustiveness from:
1. finite FinalCarrierDomain subtype;
2. generation of every FinalCarrierDomain carrier.

It does not prove the generation obligation.
-/

theorem RepositoryNativeFiniteRegistryExhaustiveness_from_fintype
    [DecidableEq ChronosCarrierData]
    [Fintype { c : ChronosCarrierData // FinalCarrierDomain c }]
    (hGen :
      ∀ c : ChronosCarrierData,
        FinalCarrierDomain c →
        RepositoryNativeGenerated c) :
    ∃ R : Finset ChronosCarrierData,
      ∀ c : ChronosCarrierData,
        FinalCarrierDomain c →
        c ∈ R ∧ RepositoryNativeGenerated c := by
  refine ⟨Finset.univ.image Subtype.val, fun c hc => ⟨?_, hGen c hc⟩⟩
  exact Finset.mem_image.mpr ⟨⟨c, hc⟩, Finset.mem_univ _, rfl⟩

axiom FinalCarrierDomain_fintype :
  Fintype { c : ChronosCarrierData // FinalCarrierDomain c }

axiom FinalCarrierDomain_repository_native_generated :
  ∀ c : ChronosCarrierData,
    FinalCarrierDomain c →
    RepositoryNativeGenerated c

noncomputable theorem RepositoryNativeFiniteRegistryExhaustiveness_from_fintype_axioms
    [DecidableEq ChronosCarrierData] :
    ∃ R : Finset ChronosCarrierData,
      ∀ c : ChronosCarrierData,
        FinalCarrierDomain c →
        c ∈ R ∧ RepositoryNativeGenerated c := by
  letI := FinalCarrierDomain_fintype
  exact RepositoryNativeFiniteRegistryExhaustiveness_from_fintype
    FinalCarrierDomain_repository_native_generated
