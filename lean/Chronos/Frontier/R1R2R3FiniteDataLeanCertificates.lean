import Chronos.Frontier.R1R2R3IsolatedTargetsConditionalClosure

namespace Chronos.Frontier

/--
Lean-native finite R1 certificate corresponding to the checked finite
long-chord data packet.

This certifies only the supplied finite packet:
max candidate skeleton distance 2 is strictly below threshold 3.
-/
def R1FiniteLongChordDataCertified : Prop :=
  (2 : Nat) < 3

theorem r1_finite_long_chord_data_certified :
    R1FiniteLongChordDataCertified :=
  by
    unfold R1FiniteLongChordDataCertified
    decide

/--
Lean-native finite R2 certificate corresponding to the checked finite
diameter/separation/filling data packet.

This certifies only the supplied finite packet:
diameter 5 <= bound 5, minimum separation 3 >= threshold 3,
and minimum filling size 3 is strictly above floor 2.
-/
def R2FiniteDiameterSeparationFillingDataCertified : Prop :=
  ((5 : Nat) <= 5) ∧ ((3 : Nat) >= 3) ∧ ((2 : Nat) < 3)

theorem r2_finite_diameter_separation_filling_data_certified :
    R2FiniteDiameterSeparationFillingDataCertified :=
  by
    unfold R2FiniteDiameterSeparationFillingDataCertified
    decide

/--
Lean-native finite R3 certificate corresponding to the checked finite
uniform local-type capacity packet.

This certifies only the supplied finite packet:
distinct local-type count 2 is at most capacity bound 2.
-/
def R3FiniteUniformLocalTypeCapacityDataCertified : Prop :=
  (2 : Nat) <= 2

theorem r3_finite_uniform_local_type_capacity_data_certified :
    R3FiniteUniformLocalTypeCapacityDataCertified :=
  by
    unfold R3FiniteUniformLocalTypeCapacityDataCertified
    decide

/--
Finite-data bundle.

This records that all three supplied finite mathematical-data packets
have Lean-native arithmetic certificates.
-/
def R1R2R3FiniteDataBundleCertified : Prop :=
  R1FiniteLongChordDataCertified ∧
  R2FiniteDiameterSeparationFillingDataCertified ∧
  R3FiniteUniformLocalTypeCapacityDataCertified

theorem r1_r2_r3_finite_data_bundle_certified :
    R1R2R3FiniteDataBundleCertified :=
  And.intro
    r1_finite_long_chord_data_certified
    (And.intro
      r2_finite_diameter_separation_filling_data_certified
      r3_finite_uniform_local_type_capacity_data_certified)

/--
Promotion gap.

Finite-data certification alone does not construct the opaque repository
native proof target `LongChordExclusionProofTarget`.
-/
def R1FiniteDataToGeneralProofPromotionGap : Prop :=
  R1FiniteLongChordDataCertified → LongChordExclusionProofTarget

/--
Promotion gap.

Finite-data certification alone does not construct the opaque repository
native proof target `DiameterSeparationFillingObstructionProofTarget`.
-/
def R2FiniteDataToGeneralProofPromotionGap : Prop :=
  R2FiniteDiameterSeparationFillingDataCertified →
  DiameterSeparationFillingObstructionProofTarget

/--
Promotion gap.

Finite-data certification alone does not construct the opaque repository
native proof target `UniformLocalTypeCapacityProofTarget`.
-/
def R3FiniteDataToGeneralProofPromotionGap : Prop :=
  R3FiniteUniformLocalTypeCapacityDataCertified →
  UniformLocalTypeCapacityProofTarget

/--
Exact theorem-level promotion object still missing after finite-data
Lean certification.
-/
def R1R2R3FiniteDataToNativeProofPromotionGap : Prop :=
  R1FiniteDataToGeneralProofPromotionGap ∧
  R2FiniteDataToGeneralProofPromotionGap ∧
  R3FiniteDataToGeneralProofPromotionGap

end Chronos.Frontier
