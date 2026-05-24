import Chronos.Frontier.R1R2R3PromotionProofTargetRegistry

namespace Chronos.Frontier

/--
OPAQUE ASSUMPTION BOUNDARY DECLARATION ONLY.

The repository-native R1/R2/R3 targets are opaque proof targets.
Finite arithmetic certificates alone do not reduce to those targets.

This file records the four missing bridge assumptions explicitly.
It does not convert those assumptions into theorem-level closure.
-/
opaque r1_finite_data_to_general_proof_promotion_assumption :
  R1FiniteLongChordDataCertified → LongChordExclusionProofTarget

opaque r2_finite_data_to_general_proof_promotion_assumption :
  R2FiniteDiameterSeparationFillingDataCertified →
    DiameterSeparationFillingObstructionProofTarget

opaque r3_finite_data_to_general_proof_promotion_assumption :
  R3FiniteUniformLocalTypeCapacityDataCertified →
    UniformLocalTypeCapacityProofTarget

opaque repository_native_r1_r2_r3_instance_to_non_factorisation_assumption :
  RepositoryNativeR1R2R3InstanceTarget → NonFactorisationProofTarget

theorem R1FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque :
    R1FiniteDataToGeneralProofPromotionAssumption :=
  r1_finite_data_to_general_proof_promotion_assumption

theorem R2FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque :
    R2FiniteDataToGeneralProofPromotionAssumption :=
  r2_finite_data_to_general_proof_promotion_assumption

theorem R3FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque :
    R3FiniteDataToGeneralProofPromotionAssumption :=
  r3_finite_data_to_general_proof_promotion_assumption

theorem NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance_declared_by_opaque :
    NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance :=
  repository_native_r1_r2_r3_instance_to_non_factorisation_assumption

theorem RepositoryNativeR1R2R3InstanceTarget_derived_under_opaque_boundary :
    RepositoryNativeR1R2R3InstanceTarget :=
  repository_native_r1_r2_r3_instance_from_finite_data_promotion_assumptions
    R1FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque
    R2FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque
    R3FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque

theorem NonFactorisationProofTarget_derived_under_opaque_boundary :
    NonFactorisationProofTarget :=
  NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance_declared_by_opaque
    RepositoryNativeR1R2R3InstanceTarget_derived_under_opaque_boundary

theorem R1R2R3PromotionProofTargetRegistry_derived_under_opaque_boundary :
    R1R2R3PromotionProofTargetRegistry :=
  And.intro
    R1FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque
    (And.intro
      R2FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque
      (And.intro
        R3FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque
        NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance_declared_by_opaque))

def R1R2R3OpaqueBoundaryDeclarationStatus : String :=
  "OPAQUE_ASSUMPTION_DECLARATION_ONLY"

def R1R2R3OpaqueBoundaryDeclarationBoundary : String :=
  "Does not prove theorem-level R1, R2, R3, NON_FACTORISATION, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem."

end Chronos.Frontier
