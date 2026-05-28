namespace Chronos.Frontier.PhysicalDetectorFieldExtractionMap

structure PhysicalDetectorField where
  detectorCount : Nat
  fieldSamples : List Nat
deriving Repr, DecidableEq

def extractedDetectorCount (x : PhysicalDetectorField) : Nat :=
  x.fieldSamples.length

def extractedActiveMass (x : PhysicalDetectorField) : Nat :=
  x.fieldSamples.foldl (fun acc m => acc + m) 0

def restrictedFiniteDetectorExtractionGate (x : PhysicalDetectorField) : Prop :=
  extractedDetectorCount x = x.fieldSamples.length

def feedsRestrictedMassRadiusGate (x : PhysicalDetectorField) : Prop :=
  restrictedFiniteDetectorExtractionGate x

theorem extracted_detector_count_def (x : PhysicalDetectorField) :
    extractedDetectorCount x = x.fieldSamples.length := rfl

theorem physical_detector_field_feeds_restricted_gate (x : PhysicalDetectorField) :
    feedsRestrictedMassRadiusGate x := rfl

theorem empty_physical_detector_field_zero_active_mass :
    extractedActiveMass { detectorCount := 0, fieldSamples := [] } = 0 := rfl

theorem empty_physical_detector_field_zero_detector_count :
    extractedDetectorCount { detectorCount := 0, fieldSamples := [] } = 0 := rfl

end Chronos.Frontier.PhysicalDetectorFieldExtractionMap


namespace Chronos.Frontier.PhysicalDetectorFieldExtractionMap

def emptyDetectorFieldWitness : PhysicalDetectorField :=
  { detectorCount := 0, fieldSamples := [] }

def oneDetectorFieldWitness : PhysicalDetectorField :=
  { detectorCount := 1, fieldSamples := [7] }

def finiteDetectorFieldWitness : PhysicalDetectorField :=
  { detectorCount := 3, fieldSamples := [2, 5, 11] }

theorem empty_detector_field_actual_values :
    extractedDetectorCount emptyDetectorFieldWitness = 0 ∧
    extractedActiveMass emptyDetectorFieldWitness = 0 ∧
    feedsRestrictedMassRadiusGate emptyDetectorFieldWitness := by
  simp [emptyDetectorFieldWitness, extractedDetectorCount, extractedActiveMass,
    feedsRestrictedMassRadiusGate, restrictedFiniteDetectorExtractionGate]

theorem one_detector_field_actual_values :
    extractedDetectorCount oneDetectorFieldWitness = 1 ∧
    extractedActiveMass oneDetectorFieldWitness = 7 ∧
    feedsRestrictedMassRadiusGate oneDetectorFieldWitness := by
  simp [oneDetectorFieldWitness, extractedDetectorCount, extractedActiveMass,
    feedsRestrictedMassRadiusGate, restrictedFiniteDetectorExtractionGate]

theorem finite_detector_field_actual_values :
    extractedDetectorCount finiteDetectorFieldWitness = 3 ∧
    extractedActiveMass finiteDetectorFieldWitness = 18 ∧
    feedsRestrictedMassRadiusGate finiteDetectorFieldWitness := by
  simp [finiteDetectorFieldWitness, extractedDetectorCount, extractedActiveMass,
    feedsRestrictedMassRadiusGate, restrictedFiniteDetectorExtractionGate]

end Chronos.Frontier.PhysicalDetectorFieldExtractionMap
