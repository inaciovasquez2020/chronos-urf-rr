import Chronos.Frontier.FinalCarrierDomainDecision
import Chronos.Frontier.IntendedChronosAdmissibility

namespace Chronos.Frontier.H4_1_FGL_Bridge1Refutation

open Chronos.Frontier.FinalCarrierDomainDecision
open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.RealChronosAdmissible

def zeroArityCarrier : ChronosCarrierData :=
  { arity := 0, stratum := 0, index := 0 }

theorem zero_arity_carrier_is_real_admissible :
    RealChronosAdmissiblePredicate
      ChronosRegistry ChronosTraceFamily zeroArityCarrier := by
  exact registered_carrier_is_real_chronos_admissible
    ChronosRegistry ChronosTraceFamily zeroArityCarrier trivial

theorem zero_arity_carrier_not_final_domain :
    ¬ FinalCarrierDomain zeroArityCarrier := by
  intro h
  exact h.2 rfl

def H4_1_FGL_AdmissibleToFinalCarrierDomain : Prop :=
  ∀ C : ChronosCarrierData,
    RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily C →
    FinalCarrierDomain C

theorem admissible_to_final_carrier_domain_false :
    ¬ H4_1_FGL_AdmissibleToFinalCarrierDomain := by
  intro h
  exact zero_arity_carrier_not_final_domain
    (h zeroArityCarrier zero_arity_carrier_is_real_admissible)

end Chronos.Frontier.H4_1_FGL_Bridge1Refutation
