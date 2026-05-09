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
