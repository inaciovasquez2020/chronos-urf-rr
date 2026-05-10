import Chronos.Frontier.ZeroPositiveRegSNFReduction

open Chronos.Frontier.CarrierRegistryExhaustivenessBridge

/--
The isolated remaining zero-arity branch after the zero-positive Reg-SNF
reduction.  This is the exact residual object needed to turn the reduction
into unrestricted Reg-SNF for real Chronos-admissible carriers.
-/
def RepresentedZeroArityRegSNF : Prop :=
  ∀ s i : Nat,
    RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily
      { arity := 0, stratum := s, index := i } →
    RegSNF ChronosRegistry ChronosTraceFamily
      { arity := 0, stratum := s, index := i }

/--
If represented zero-arity Reg-SNF is supplied, the existing zero-positive
reduction closes unrestricted Reg-SNF over real Chronos-admissible carriers.
-/
theorem represented_zero_arity_reg_snf_implies_unrestricted_reg_snf
    (hZero : RepresentedZeroArityRegSNF) :
    ∀ C : ChronosCarrierData,
      RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily C →
      RegSNF ChronosRegistry ChronosTraceFamily C := by
  intro C hC
  exact zero_positive_reg_snf_reduction hZero C hC

/--
Status lock: the represented zero-arity branch is now the isolated remaining
frontier for this route, not ZeroArityExclusion.
-/
def RepresentedZeroArityRegSNFFrontierOpen : Prop :=
  RepresentedZeroArityRegSNF

/--
The zero-positive reduction records the represented zero-arity branch as the
weakest remaining assumption for unrestricted Reg-SNF.
-/
theorem represented_zero_arity_reg_snf_frontier_records_reduction :
    RepresentedZeroArityRegSNF →
      ∀ C : ChronosCarrierData,
        RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily C →
        RegSNF ChronosRegistry ChronosTraceFamily C := by
  intro hZero C hC
  exact represented_zero_arity_reg_snf_implies_unrestricted_reg_snf hZero C hC
