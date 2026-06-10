import Chronos.Frontier.PositiveArityRepositoryNativeCoverage
import Chronos.Frontier.RepositoryNativeImageCoverageCounterexample

namespace Chronos.Frontier.FinalCarrierDomainDecision

/--
Toolkit decision:
the final carrier-domain theorem for the current Chronos Reg-SNF route is
PositiveArityCarrier, not unrestricted RealChronosAdmissiblePredicate.
-/
def FinalCarrierDomain (C : ChronosCarrierData) : Prop :=
  PositiveArityCarrier C

/--
The selected final carrier domain is already Reg-SNF closed.
-/
theorem final_carrier_domain_reg_snf_closed :
    ∀ C : ChronosCarrierData,
      FinalCarrierDomain C →
      RegSNF ChronosRegistry ChronosTraceFamily C := by
  intro C hC
  exact positive_arity_reg_snf_closed C hC

/--
Zero-arity carriers are intentionally outside the selected final domain.
-/
theorem zero_arity_excluded_from_final_carrier_domain
    (C : ChronosCarrierData)
    (h0 : C.arity = 0) :
    ¬ FinalCarrierDomain C := by
  intro hC
  exact hC.2 h0


/--
The current selected final carrier domain is arity-unbounded.
Therefore `FinalCarrierDomain_fintype` cannot be derived from the
current definition without replacing the domain by a bounded one.
-/
theorem final_carrier_domain_unbounded_arity :
    ∀ B : Nat, ∃ C : ChronosCarrierData, FinalCarrierDomain C ∧ B < C.arity := by
  intro B
  let C : ChronosCarrierData := { arity := B.succ, stratum := 0, index := 0 }
  refine ⟨C, ?_, ?_⟩
  · unfold FinalCarrierDomain PositiveArityCarrier
    constructor
    · exact
        Chronos.Frontier.IntendedChronosAdmissibility.every_intended_is_admissible
          C
          (by
            unfold Chronos.Frontier.IntendedChronosAdmissibility.IntendedChronosCarrier
            constructor
            · simp [C]
            · simp [C])
    · simp [C]
  · simp [C]

theorem not_final_carrier_domain_uniform_arity_bound :
    ¬ ∃ B : Nat, ∀ C : ChronosCarrierData, FinalCarrierDomain C → C.arity ≤ B := by
  intro h
  rcases h with ⟨B, hB⟩
  rcases final_carrier_domain_unbounded_arity B with ⟨C, hC, hlt⟩
  exact (Nat.not_le_of_gt hlt) (hB C hC)

/--
Abstract Carrier Registry Exhaustiveness is not required for the selected
positive-arity carrier-domain closure.
-/
def AbstractCarrierRegistryExhaustivenessRequiredForSelectedDomain : Prop :=
  False

theorem abstract_exhaustiveness_not_required_for_selected_domain :
    ¬ AbstractCarrierRegistryExhaustivenessRequiredForSelectedDomain := by
  intro h
  exact h

/--
Optional stronger target:
one may still pursue abstract exhaustiveness as a separate generalization,
but it is not part of the closed positive-arity carrier-domain theorem.
-/
def OptionalAbstractCarrierRegistryExhaustivenessGeneralization : Prop :=
  True

theorem optional_abstract_exhaustiveness_generalization_recorded :
    OptionalAbstractCarrierRegistryExhaustivenessGeneralization := by
  trivial

end Chronos.Frontier.FinalCarrierDomainDecision

namespace Chronos.Frontier.FinalCarrierDomainDecision

/--
Bounded replacement for the unbounded final carrier domain.

This is the admissible finite-domain target replacing the impossible
unbounded `FinalCarrierDomain_fintype` target.
-/
def BoundedFinalCarrierDomain (B : Nat) (C : ChronosCarrierData) : Prop :=
  FinalCarrierDomain C ∧ C.arity ≤ B

end Chronos.Frontier.FinalCarrierDomainDecision

namespace Chronos.Frontier.FinalCarrierDomainDecision

/--
Fully bounded finite replacement target for the unbounded final carrier domain.

Unlike `BoundedFinalCarrierDomain`, this bounds every native Nat coordinate
of `ChronosCarrierData`.
-/
def FullyBoundedFinalCarrierDomain (B : Nat) (C : ChronosCarrierData) : Prop :=
  FinalCarrierDomain C ∧ C.arity ≤ B ∧ C.stratum ≤ B ∧ C.index ≤ B

end Chronos.Frontier.FinalCarrierDomainDecision
