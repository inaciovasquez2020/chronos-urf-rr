import Chronos.Frontier.RepresentedZeroArityRegSNFFrontier

open Chronos.Frontier.CarrierRegistryExhaustivenessBridge
open Chronos.Frontier.RealChronosAdmissible
open Chronos.Frontier.IntendedChronosAdmissibility

theorem represented_zero_arity_reg_snf_closed :
    RepresentedZeroArityRegSNF := by
  intro s i hC
  exact real_chronos_admissible_predicate_implies_reg_snf
    ChronosRegistry ChronosTraceFamily
    { arity := 0, stratum := s, index := i }
    hC

theorem unrestricted_real_chronos_admissible_reg_snf_closed :
    ∀ C : ChronosCarrierData,
      RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily C →
      RegSNF ChronosRegistry ChronosTraceFamily C := by
  exact represented_zero_arity_reg_snf_implies_unrestricted_reg_snf
    represented_zero_arity_reg_snf_closed
