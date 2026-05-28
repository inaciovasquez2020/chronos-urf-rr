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
