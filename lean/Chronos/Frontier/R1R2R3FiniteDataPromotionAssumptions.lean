import Chronos.Frontier.R1R2R3FiniteDataLeanCertificates

namespace Chronos.Frontier

/--
R1 promotion assumption.

This is an explicit assumption converting the finite checked long-chord
data certificate into the repository-native R1 proof target.

It is not proved here.
-/
def R1FiniteDataToGeneralProofPromotionAssumption : Prop :=
  R1FiniteDataToGeneralProofPromotionGap

/--
R2 promotion assumption.

This is an explicit assumption converting the finite checked
diameter/separation/filling data certificate into the repository-native
R2 proof target.

It is not proved here.
-/
def R2FiniteDataToGeneralProofPromotionAssumption : Prop :=
  R2FiniteDataToGeneralProofPromotionGap

/--
R3 promotion assumption.

This is an explicit assumption converting the finite checked uniform
local-type capacity data certificate into the repository-native R3 proof
target.

It is not proved here.
-/
def R3FiniteDataToGeneralProofPromotionAssumption : Prop :=
  R3FiniteDataToGeneralProofPromotionGap

theorem r1_native_target_from_finite_data_promotion_assumption
    (hR1 : R1FiniteDataToGeneralProofPromotionAssumption) :
    LongChordExclusionProofTarget :=
  hR1 r1_finite_long_chord_data_certified

theorem r2_native_target_from_finite_data_promotion_assumption
    (hR2 : R2FiniteDataToGeneralProofPromotionAssumption) :
    DiameterSeparationFillingObstructionProofTarget :=
  hR2 r2_finite_diameter_separation_filling_data_certified

theorem r3_native_target_from_finite_data_promotion_assumption
    (hR3 : R3FiniteDataToGeneralProofPromotionAssumption) :
    UniformLocalTypeCapacityProofTarget :=
  hR3 r3_finite_uniform_local_type_capacity_data_certified

/--
Conditional native R1/R2/R3 instance assembly.

The native instance target is assembled only from the three explicit
promotion assumptions.  This does not prove the assumptions.
-/
theorem repository_native_r1_r2_r3_instance_from_finite_data_promotion_assumptions
    (hR1 : R1FiniteDataToGeneralProofPromotionAssumption)
    (hR2 : R2FiniteDataToGeneralProofPromotionAssumption)
    (hR3 : R3FiniteDataToGeneralProofPromotionAssumption) :
    RepositoryNativeR1R2R3InstanceTarget :=
  And.intro
    (r1_native_target_from_finite_data_promotion_assumption hR1)
    (And.intro
      (r2_native_target_from_finite_data_promotion_assumption hR2)
      (r3_native_target_from_finite_data_promotion_assumption hR3))

/--
NON_FACTORISATION remains conditional on a native R1/R2/R3 instance.
-/
def NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance : Prop :=
  RepositoryNativeR1R2R3InstanceTarget → NonFactorisationProofTarget

theorem non_factorisation_from_native_r1_r2_r3_instance_conditional
    (hNF : NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance)
    (hInst : RepositoryNativeR1R2R3InstanceTarget) :
    NonFactorisationProofTarget :=
  hNF hInst

/--
Full conditional surface.

Given the three finite-data promotion assumptions and a separate
conditional non-factorisation bridge from a native R1/R2/R3 instance,
NON_FACTORISATION follows.

This does not prove the promotion assumptions or the non-factorisation
bridge.
-/
theorem non_factorisation_from_finite_data_promotion_assumptions_conditional
    (hR1 : R1FiniteDataToGeneralProofPromotionAssumption)
    (hR2 : R2FiniteDataToGeneralProofPromotionAssumption)
    (hR3 : R3FiniteDataToGeneralProofPromotionAssumption)
    (hNF : NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance) :
    NonFactorisationProofTarget :=
  hNF
    (repository_native_r1_r2_r3_instance_from_finite_data_promotion_assumptions
      hR1 hR2 hR3)

/--
Exact remaining theorem-level object after this layer.
-/
def R1R2R3PromotionAssumptionsToNonFactorisationConditionalSurface : Prop :=
  R1FiniteDataToGeneralProofPromotionAssumption →
  R2FiniteDataToGeneralProofPromotionAssumption →
  R3FiniteDataToGeneralProofPromotionAssumption →
  NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance →
  NonFactorisationProofTarget

theorem r1_r2_r3_promotion_assumptions_to_non_factorisation_conditional_surface :
    R1R2R3PromotionAssumptionsToNonFactorisationConditionalSurface :=
  by
    intro hR1 hR2 hR3 hNF
    exact non_factorisation_from_finite_data_promotion_assumptions_conditional
      hR1 hR2 hR3 hNF

end Chronos.Frontier
