import Chronos.Frontier.R1R2R3PromotionProofTargetRegistry

namespace Chronos.Frontier

/--
CONDITIONAL ASSUMPTION SURFACE ONLY.

The repository-native R1/R2/R3 targets are opaque proof targets.
Finite arithmetic certificates alone do not reduce to those targets.

This file records the four missing bridges as a Prop-valued assumption
surface and proves only conditional assembly from that surface.

It introduces no `axiom` declarations and no `opaque` declarations.
It does not close R1, R2, R3, or NON_FACTORISATION theorem-level targets.
-/
def R1FiniteDataToGeneralProofPromotionBridgeAssumption : Prop :=
  R1FiniteLongChordDataCertified → LongChordExclusionProofTarget

def R2FiniteDataToGeneralProofPromotionBridgeAssumption : Prop :=
  R2FiniteDiameterSeparationFillingDataCertified →
    DiameterSeparationFillingObstructionProofTarget

def R3FiniteDataToGeneralProofPromotionBridgeAssumption : Prop :=
  R3FiniteUniformLocalTypeCapacityDataCertified →
    UniformLocalTypeCapacityProofTarget

def RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumption : Prop :=
  RepositoryNativeR1R2R3InstanceTarget → NonFactorisationProofTarget

structure R1R2R3ConditionalAssumptionSurface : Prop where
  r1 : R1FiniteDataToGeneralProofPromotionBridgeAssumption
  r2 : R2FiniteDataToGeneralProofPromotionBridgeAssumption
  r3 : R3FiniteDataToGeneralProofPromotionBridgeAssumption
  nonfactorisation : RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumption

theorem R1FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface
    (h : R1R2R3ConditionalAssumptionSurface) :
    R1FiniteDataToGeneralProofPromotionAssumption :=
  h.r1

theorem R2FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface
    (h : R1R2R3ConditionalAssumptionSurface) :
    R2FiniteDataToGeneralProofPromotionAssumption :=
  h.r2

theorem R3FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface
    (h : R1R2R3ConditionalAssumptionSurface) :
    R3FiniteDataToGeneralProofPromotionAssumption :=
  h.r3

theorem NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance_conditional_on_surface
    (h : R1R2R3ConditionalAssumptionSurface) :
    NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance :=
  h.nonfactorisation

theorem RepositoryNativeR1R2R3InstanceTarget_conditional_on_surface
    (h : R1R2R3ConditionalAssumptionSurface) :
    RepositoryNativeR1R2R3InstanceTarget :=
  repository_native_r1_r2_r3_instance_from_finite_data_promotion_assumptions
    (R1FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface h)
    (R2FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface h)
    (R3FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface h)

theorem NonFactorisationProofTarget_conditional_on_surface
    (h : R1R2R3ConditionalAssumptionSurface) :
    NonFactorisationProofTarget :=
  h.nonfactorisation
    (RepositoryNativeR1R2R3InstanceTarget_conditional_on_surface h)

theorem R1R2R3PromotionProofTargetRegistry_conditional_on_surface
    (h : R1R2R3ConditionalAssumptionSurface) :
    R1R2R3PromotionProofTargetRegistry :=
  And.intro
    (R1FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface h)
    (And.intro
      (R2FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface h)
      (And.intro
        (R3FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface h)
        (NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance_conditional_on_surface h)))

def R1R2R3ConditionalAssumptionSurfaceStatus : String :=
  "CONDITIONAL_ASSUMPTION_SURFACE_ONLY_NOT_CLOSURE"

def R1R2R3ConditionalAssumptionSurfaceBoundary : String :=
  "Does not prove theorem-level R1, R2, R3, NON_FACTORISATION, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem."

end Chronos.Frontier
