import Chronos.Frontier.NewtonianEqualOppositeGravityForceActualValueTest
import Chronos.Frontier.PhysicalDetectorFieldExtractionMap

namespace Chronos.Frontier.NewtonianForceDetectorCoherenceBridge

open Chronos.Frontier.NewtonianEqualOppositeGravityForceActualValueTest
open Chronos.Frontier.PhysicalDetectorFieldExtractionMap

def detectorFieldFromNewtonianSample (x : NewtonianTwoBodySample) :
    PhysicalDetectorField :=
  { detectorCount := 2,
    fieldSamples := [commonForceMagnitude x, commonForceMagnitude x] }

def detectorCoherentWithNewtonianForce (x : NewtonianTwoBodySample) : Prop :=
  feedsRestrictedMassRadiusGate (detectorFieldFromNewtonianSample x) ∧
  extractedDetectorCount (detectorFieldFromNewtonianSample x) = 2 ∧
  extractedActiveMass (detectorFieldFromNewtonianSample x) =
    commonForceMagnitude x + commonForceMagnitude x ∧
  equalAndOppositeForces x

theorem detector_field_from_newtonian_sample_gate
    (x : NewtonianTwoBodySample) :
    feedsRestrictedMassRadiusGate (detectorFieldFromNewtonianSample x) := by
  simp [detectorFieldFromNewtonianSample, feedsRestrictedMassRadiusGate,
    restrictedFiniteDetectorExtractionGate, extractedDetectorCount]

theorem newtonian_force_detector_coherence_bridge
    (x : NewtonianTwoBodySample) :
    detectorCoherentWithNewtonianForce x := by
  simp [detectorCoherentWithNewtonianForce, detectorFieldFromNewtonianSample,
    feedsRestrictedMassRadiusGate, restrictedFiniteDetectorExtractionGate,
    extractedDetectorCount, extractedActiveMass, equalAndOppositeForces,
    forceOnAByB, forceOnBByA]

theorem actual_earth_moon_scaled_detector_coherence_values :
    extractedDetectorCount
      (detectorFieldFromNewtonianSample actualEarthMoonScaledWitness) = 2 ∧
    extractedActiveMass
      (detectorFieldFromNewtonianSample actualEarthMoonScaledWitness) = 72 ∧
    detectorCoherentWithNewtonianForce actualEarthMoonScaledWitness := by
  simp [detectorFieldFromNewtonianSample, actualEarthMoonScaledWitness,
    commonForceMagnitude, extractedDetectorCount, extractedActiveMass,
    detectorCoherentWithNewtonianForce, feedsRestrictedMassRadiusGate,
    restrictedFiniteDetectorExtractionGate, equalAndOppositeForces,
    forceOnAByB, forceOnBByA]

theorem actual_balanced_unit_detector_coherence_values :
    extractedDetectorCount
      (detectorFieldFromNewtonianSample actualBalancedUnitWitness) = 2 ∧
    extractedActiveMass
      (detectorFieldFromNewtonianSample actualBalancedUnitWitness) = 60 ∧
    detectorCoherentWithNewtonianForce actualBalancedUnitWitness := by
  simp [detectorFieldFromNewtonianSample, actualBalancedUnitWitness,
    commonForceMagnitude, extractedDetectorCount, extractedActiveMass,
    detectorCoherentWithNewtonianForce, feedsRestrictedMassRadiusGate,
    restrictedFiniteDetectorExtractionGate, equalAndOppositeForces,
    forceOnAByB, forceOnBByA]

end Chronos.Frontier.NewtonianForceDetectorCoherenceBridge
