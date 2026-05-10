import Chronos.Frontier.ZeroPositiveCarrierCaseSplit
import Chronos.Frontier.FinalCarrierDomainDecision

open Chronos.Frontier.CarrierRegistryExhaustivenessBridge
open Chronos.Frontier.PositiveArityRepositoryNativeCoverage

/--
Reduction: unrestricted Reg-SNF over real Chronos-admissible carriers reduces to
the represented zero-arity cases, since the positive-arity branch is already
closed by `positive_arity_reg_snf_closed`.
-/
theorem zero_positive_reg_snf_reduction
    (hZero :
      ∀ s i : Nat,
        RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily
          { arity := 0, stratum := s, index := i } →
        RegSNF ChronosRegistry ChronosTraceFamily
          { arity := 0, stratum := s, index := i })
    (C : ChronosCarrierData)
    (hC : RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily C) :
    RegSNF ChronosRegistry ChronosTraceFamily C := by
  refine zero_positive_carrier_case_split
    (fun D => RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily D →
      RegSNF ChronosRegistry ChronosTraceFamily D)
    ?zero
    ?positive
    C
    hC
  · intro s i
    exact hZero s i
  · intro D hpos hD
    exact positive_arity_reg_snf_closed D ⟨hD, Nat.ne_of_gt hpos⟩
