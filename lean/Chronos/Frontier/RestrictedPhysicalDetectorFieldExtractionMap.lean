import Mathlib

namespace Chronos
namespace Frontier
namespace RestrictedPhysicalDetectorFieldExtractionMap

/--
A restricted physical detector field is a finite, discrete physical sampling
profile.  This deliberately avoids continuum GR/PDE claims: the only physical
input admitted here is a finite detector-indexed profile of natural-valued
readings, radii, and active flags.
-/
structure PhysicalDetectorField (Detector : Type*) where
  reading : Detector → ℕ
  radius : Detector → ℕ
  active : Detector → Bool


/-- The finite active detector family extracted from the physical profile. -/
def activeDetectors {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector) : Finset Detector :=
  Finset.univ.filter (fun d => F.active d = true)

/-- Membership in the extracted active detector family is exactly the active flag. -/
theorem physicalExtraction_activeSet_correct
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector) (d : Detector) :
    d ∈ activeDetectors F ↔ F.active d = true := by
  simp [activeDetectors]

/--
Atomic detector mass extracted from the physical profile.

Inactive detectors contribute zero.  Active detectors contribute their declared
natural-valued physical reading.
-/
def physicalAtomMass {Detector : Type*}
    (F : PhysicalDetectorField Detector) (d : Detector) : ℕ :=
  match F.active d with
  | true => F.reading d
  | false => 0

/-- The finite multiradius support induced by active detectors. -/
def activeRadiusValues {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector) : Finset ℕ :=
  (activeDetectors F).image F.radius

/--
The extracted radius floor: finite minimum of active radii when present,
and zero when no active radius exists.
-/
def extractedRadiusFloor {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector) : ℕ :=
  if h : (activeRadiusValues F).Nonempty then
    (activeRadiusValues F).min' h
  else
    0

/-- The extracted active mass is the finite sum of active atomic masses. -/
def extractedActiveMass {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector) : ℕ :=
  (activeDetectors F).sum (physicalAtomMass F)

/-- Finite detector data produced by the restricted physical extraction map. -/
structure ExtractedFiniteDetectorData where
  atoms : Finset ℕ
  activeMass : ℕ
  radiusFloor : ℕ

/-- The restricted physical-to-finite extraction map. -/
def extractFiniteDetectorData
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector) : ExtractedFiniteDetectorData where
  atoms := (activeDetectors F).image (physicalAtomMass F)
  activeMass := extractedActiveMass F
  radiusFloor := extractedRadiusFloor F

/--
Restricted finite detector gate.

This is intentionally finite and interface-level.  It is not a continuum
gravity theorem.
-/
def RestrictedFiniteDetectorGate (activeMass radiusFloor : ℕ) : Prop :=
  activeMass ≤ radiusFloor

/--
Corrected boundary admissibility.

The aggregate gate bound is an explicit structural assumption at the physical
boundary.  It is not derived from pointwise reading/radius bounds.
-/
structure PhysicalDetectorFieldAdmissible
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector) : Prop where
  gate_bound :
    RestrictedFiniteDetectorGate
      (extractedActiveMass F)
      (extractedRadiusFloor F)

/--
Active mass coherence: the extracted active mass equals the finite sum of
declared physical readings over the extracted active set.
-/
theorem physicalExtraction_atomMass_coherent
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector) :
    extractedActiveMass F = (activeDetectors F).sum F.reading := by
  unfold extractedActiveMass
  apply Finset.sum_congr rfl
  intro d hd
  have hactive : F.active d = true :=
    (physicalExtraction_activeSet_correct F d).mp hd
  simp [physicalAtomMass, hactive]

/-- The extracted data stores the extracted active mass definitionally. -/
theorem physicalExtraction_data_activeMass
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector) :
    (extractFiniteDetectorData F).activeMass = extractedActiveMass F := by
  rfl

/-- The extracted data stores the extracted radius floor definitionally. -/
theorem physicalExtraction_data_radiusFloor
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector) :
    (extractFiniteDetectorData F).radiusFloor = extractedRadiusFloor F := by
  rfl

/--
Bridge theorem: admissible restricted physical detector fields feed the
restricted finite detector gate.

This is conditional on `gate_bound`; it does not prove that arbitrary physical
fields satisfy the bound.
-/
theorem physicalExtraction_feeds_restrictedFiniteDetectorGate
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector)
    (hF : PhysicalDetectorFieldAdmissible F) :
    RestrictedFiniteDetectorGate
      (extractedActiveMass F)
      (extractedRadiusFloor F) := by
  exact hF.gate_bound

end RestrictedPhysicalDetectorFieldExtractionMap
end Frontier
end Chronos
