import Chronos.Frontier.NewtonianForceDetectorCoherenceBridge

namespace Chronos.Frontier.FiniteScalingInvarianceOfDetectorExtraction

open Chronos.Frontier.NewtonianEqualOppositeGravityForceActualValueTest
open Chronos.Frontier.PhysicalDetectorFieldExtractionMap
open Chronos.Frontier.NewtonianForceDetectorCoherenceBridge

def detectorExtractedActiveMassFromNewtonianSample
    (x : NewtonianTwoBodySample) : Nat :=
  extractedActiveMass (detectorFieldFromNewtonianSample x)

theorem detector_extracted_active_mass_eq_common_force_sum
    (x : NewtonianTwoBodySample) :
    detectorExtractedActiveMassFromNewtonianSample x =
      commonForceMagnitude x + commonForceMagnitude x := by
  simp [detectorExtractedActiveMassFromNewtonianSample,
    detectorFieldFromNewtonianSample, extractedActiveMass]

theorem finite_scaling_invariance_of_detector_extraction
    (x y : NewtonianTwoBodySample)
    (k : Nat)
    (h_scale : commonForceMagnitude x = k * commonForceMagnitude y) :
    detectorExtractedActiveMassFromNewtonianSample x =
      k * detectorExtractedActiveMassFromNewtonianSample y := by
  simp [detectorExtractedActiveMassFromNewtonianSample,
    detectorFieldFromNewtonianSample, extractedActiveMass,
    h_scale, Nat.left_distrib]

def actualForceMagnitude60Witness : NewtonianTwoBodySample :=
  { massA := 10, massB := 4, distanceSquared := 2, gravitationalScale := 3 }

def actualForceMagnitude72Witness : NewtonianTwoBodySample :=
  { massA := 8, massB := 3, distanceSquared := 3, gravitationalScale := 9 }

def actualForceMagnitude90Witness : NewtonianTwoBodySample :=
  { massA := 10, massB := 3, distanceSquared := 1, gravitationalScale := 3 }

theorem actual_60_to_30_detector_scaling_values :
    commonForceMagnitude actualForceMagnitude60Witness = 60 ∧
    detectorExtractedActiveMassFromNewtonianSample actualForceMagnitude60Witness = 120 ∧
    detectorExtractedActiveMassFromNewtonianSample actualForceMagnitude60Witness =
      2 * detectorExtractedActiveMassFromNewtonianSample actualBalancedUnitWitness := by
  simp [actualForceMagnitude60Witness, actualBalancedUnitWitness,
    commonForceMagnitude, detectorExtractedActiveMassFromNewtonianSample,
    detectorFieldFromNewtonianSample, extractedActiveMass]

theorem actual_72_to_36_detector_scaling_values :
    commonForceMagnitude actualForceMagnitude72Witness = 72 ∧
    detectorExtractedActiveMassFromNewtonianSample actualForceMagnitude72Witness = 144 ∧
    detectorExtractedActiveMassFromNewtonianSample actualForceMagnitude72Witness =
      2 * detectorExtractedActiveMassFromNewtonianSample actualEarthMoonScaledWitness := by
  simp [actualForceMagnitude72Witness, actualEarthMoonScaledWitness,
    commonForceMagnitude, detectorExtractedActiveMassFromNewtonianSample,
    detectorFieldFromNewtonianSample, extractedActiveMass]

theorem actual_90_to_30_detector_scaling_values :
    commonForceMagnitude actualForceMagnitude90Witness = 90 ∧
    detectorExtractedActiveMassFromNewtonianSample actualForceMagnitude90Witness = 180 ∧
    detectorExtractedActiveMassFromNewtonianSample actualForceMagnitude90Witness =
      3 * detectorExtractedActiveMassFromNewtonianSample actualBalancedUnitWitness := by
  simp [actualForceMagnitude90Witness, actualBalancedUnitWitness,
    commonForceMagnitude, detectorExtractedActiveMassFromNewtonianSample,
    detectorFieldFromNewtonianSample, extractedActiveMass]

end Chronos.Frontier.FiniteScalingInvarianceOfDetectorExtraction
