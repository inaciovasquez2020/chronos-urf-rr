import Chronos.Frontier.RepositoryNativeFiniteRegistryExhaustivenessFromFintype
import Chronos.Frontier.FinalCarrierDomainDecision
import Chronos.Frontier.PositiveArityRepositoryNativeCoverage

/-
Independent finite-registry exhaustiveness reduction.

This proves the generation obligation from the selected final carrier domain
and positive-arity repository-native coverage, then derives finite-registry
exhaustiveness using only the existing finite-domain axiom.

It does not use RepositoryNativeFiniteRegistryExhaustiveness.
-/

theorem FinalCarrierDomain_repository_native_generated_independent :
    ∀ c : ChronosCarrierData,
      FinalCarrierDomain c →
      RepositoryNativeGenerated c := by
  intro c hc
  exact positive_arity_repository_native_image_covers c (by
    simpa [FinalCarrierDomain] using hc)

noncomputable theorem RepositoryNativeFiniteRegistryExhaustiveness_independent
    [DecidableEq ChronosCarrierData] :
    ∃ R : Finset ChronosCarrierData,
      ∀ c : ChronosCarrierData,
        FinalCarrierDomain c →
        c ∈ R ∧ RepositoryNativeGenerated c := by
  letI := FinalCarrierDomain_fintype
  exact RepositoryNativeFiniteRegistryExhaustiveness_from_fintype
    FinalCarrierDomain_repository_native_generated_independent
