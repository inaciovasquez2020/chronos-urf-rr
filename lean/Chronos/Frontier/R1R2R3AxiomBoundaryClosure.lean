import Chronos.Frontier.R1R2R3PromotionProofTargetRegistry

namespace Chronos.Frontier

/--
AXIOM BOUNDARY.

The repository-native R1/R2/R3 targets are opaque proof targets.
Finite arithmetic certificates alone do not reduce to those targets.
This file closes the registry only by making the four missing bridges explicit
as axioms.

This is not theorem-level R1, R2, R3, or NON_FACTORISATION closure.
-/
axiom r1_finite_data_to_general_proof_promotion_axiom :
  R1FiniteLongChordDataCertified → LongChordExclusionProofTarget

axiom r2_finite_data_to_general_proof_promotion_axiom :
  R2FiniteDiameterSeparationFillingDataCertified →
    DiameterSeparationFillingObstructionProofTarget

axiom r3_finite_data_to_general_proof_promotion_axiom :
  R3FiniteUniformLocalTypeCapacityDataCertified →
    UniformLocalTypeCapacityProofTarget

axiom repository_native_r1_r2_r3_instance_to_non_factorisation_axiom :
  RepositoryNativeR1R2R3InstanceTarget → NonFactorisationProofTarget

theorem R1FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom :
    R1FiniteDataToGeneralProofPromotionAssumption :=
  r1_finite_data_to_general_proof_promotion_axiom

theorem R2FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom :
    R2FiniteDataToGeneralProofPromotionAssumption :=
  r2_finite_data_to_general_proof_promotion_axiom

theorem R3FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom :
    R3FiniteDataToGeneralProofPromotionAssumption :=
  r3_finite_data_to_general_proof_promotion_axiom

theorem NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance_closed_by_axiom :
    NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance :=
  repository_native_r1_r2_r3_instance_to_non_factorisation_axiom

theorem RepositoryNativeR1R2R3InstanceTarget_closed_by_axiom_boundary :
    RepositoryNativeR1R2R3InstanceTarget :=
  repository_native_r1_r2_r3_instance_from_finite_data_promotion_assumptions
    R1FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom
    R2FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom
    R3FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom

theorem NonFactorisationProofTarget_closed_by_axiom_boundary :
    NonFactorisationProofTarget :=
  NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance_closed_by_axiom
    RepositoryNativeR1R2R3InstanceTarget_closed_by_axiom_boundary

theorem R1R2R3PromotionProofTargetRegistry_closed_by_axiom_boundary :
    R1R2R3PromotionProofTargetRegistry :=
  And.intro
    R1FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom
    (And.intro
      R2FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom
      (And.intro
        R3FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom
        NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance_closed_by_axiom))

def R1R2R3AxiomBoundaryClosureStatus : String :=
  "CLOSED_BY_EXPLICIT_AXIOM_BOUNDARY_NOT_THEOREM_LEVEL"

def R1R2R3AxiomBoundaryClosureBoundary : String :=
  "Does not prove theorem-level R1, R2, R3, NON_FACTORISATION, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem."

end Chronos.Frontier
