import Chronos.Frontier.PartitionedBudgetPhysicalDetectorGateBound
import Chronos.Frontier.ObservedRotationCurveResidualBridge

namespace Chronos
namespace Frontier
namespace RestrictedPhysicalDetectorFieldExtractionMap

/--
A restricted finite detector field enriched with integer-valued rotation-curve
dynamics. This is still a finite accounting interface: it does not assert an
empirical galaxy fit, lensing fit, continuum GR theorem, or dark-matter
replacement claim.
-/
structure PhysicalDetectorFieldWithDynamics (Detector : Type*) extends
    PhysicalDetectorField Detector where
  G : ℕ
  velocity : Detector → ℕ
  baryonicMass : Detector → ℕ
  hG : 0 < G

/--
Integer-valued required mass from the rotation-curve formula

  M_required = v^2 r / G.

The natural-number division is an intentionally restricted finite accounting
approximation.
-/
def requiredMassFromRotation
    {Detector : Type*}
    (F : PhysicalDetectorFieldWithDynamics Detector)
    (d : Detector) : ℕ :=
  (F.velocity d * F.velocity d * F.toPhysicalDetectorField.radius d) / F.G

/--
Finite detector GDM budget contribution:

  max(0, M_required - M_b).

For natural numbers, subtraction is truncated at zero, but `max 0` keeps the
intended residual-budget form explicit.
-/
def physicalGDMBudget
    {Detector : Type*}
    (F : PhysicalDetectorFieldWithDynamics Detector)
    (d : Detector) : ℕ :=
  max 0 (requiredMassFromRotation F d - F.baryonicMass d)

/--
Observed rotation-curve dynamics produce the partitioned budget certificate
required by the #542 gate bridge, provided the pointwise reading bound and
local partition bound are supplied.
-/
def physicalGDMBudget_partitioned_certificate_from_observed_rotation_curve
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorFieldWithDynamics Detector)
    (hReading :
      ∀ d,
        d ∈ activeDetectors F.toPhysicalDetectorField →
          F.toPhysicalDetectorField.reading d ≤ physicalGDMBudget F d)
    (hPartition :
      ∀ d,
        d ∈ activeDetectors F.toPhysicalDetectorField →
          physicalGDMBudget F d *
              (activeDetectors F.toPhysicalDetectorField).card
            ≤ extractedRadiusFloor F.toPhysicalDetectorField) :
    PartitionedPhysicalDetectorBudgetCertificate F.toPhysicalDetectorField where
  budget := fun d => physicalGDMBudget F d
  reading_le_budget := hReading
  budget_le_partition := hPartition

/--
Final restricted composition:

observed rotation-curve budget control
  → partitioned physical detector budget certificate
  → restricted finite detector gate.
-/
theorem physicalGDM_observed_rotation_curve_feeds_gate
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorFieldWithDynamics Detector)
    (hReading :
      ∀ d,
        d ∈ activeDetectors F.toPhysicalDetectorField →
          F.toPhysicalDetectorField.reading d ≤ physicalGDMBudget F d)
    (hPartition :
      ∀ d,
        d ∈ activeDetectors F.toPhysicalDetectorField →
          physicalGDMBudget F d *
              (activeDetectors F.toPhysicalDetectorField).card
            ≤ extractedRadiusFloor F.toPhysicalDetectorField) :
    RestrictedFiniteDetectorGate
      (extractedActiveMass F.toPhysicalDetectorField)
      (extractedRadiusFloor F.toPhysicalDetectorField) := by
  exact partitionedBudgetCertificate_feeds_restrictedFiniteDetectorGate_derived
    F.toPhysicalDetectorField
    (physicalGDMBudget_partitioned_certificate_from_observed_rotation_curve
      F hReading hPartition)

end RestrictedPhysicalDetectorFieldExtractionMap
end Frontier
end Chronos
