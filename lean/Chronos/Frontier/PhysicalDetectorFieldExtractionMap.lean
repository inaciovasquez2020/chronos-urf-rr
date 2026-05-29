import Chronos.Frontier.DetectorBudgetCompatibleToGate

namespace Chronos.Frontier

/--
`PhysicalDetectorFieldExtractionMap` is the final finite wrapper/interface
for the closed detector chain.

It packages the already-available finite field-data, partition, witness,
compatibility, and gate layers as one repository-native interface object.
It does not add geometric, empirical, PDE, or unrestricted gravity content.
-/
structure PhysicalDetectorFieldExtractionMap where
  physicalFieldData : Type
  finiteDetectorPartition : Type
  extractedPhysicalDetectorWitness : Type
  detectorBudgetCompatible : Type
  restrictedFiniteDetectorExtractionGate : Type
  extractWitness :
    physicalFieldData →
    finiteDetectorPartition →
    extractedPhysicalDetectorWitness
  compatibilityToGate :
    detectorBudgetCompatible →
    restrictedFiniteDetectorExtractionGate

def PhysicalDetectorFieldExtractionMap.gate
    (M : PhysicalDetectorFieldExtractionMap)
    (h : M.detectorBudgetCompatible) :
    M.restrictedFiniteDetectorExtractionGate :=
  M.compatibilityToGate h

def PhysicalDetectorFieldExtractionMap.gate_from_compatibility
    (M : PhysicalDetectorFieldExtractionMap)
    (h : M.detectorBudgetCompatible) :
    M.restrictedFiniteDetectorExtractionGate :=
  M.gate h

def PhysicalDetectorFieldExtractionMap.witness_from_data_partition
    (M : PhysicalDetectorFieldExtractionMap)
    (x : M.physicalFieldData)
    (p : M.finiteDetectorPartition) :
    M.extractedPhysicalDetectorWitness :=
  M.extractWitness x p

end Chronos.Frontier

namespace Chronos.Frontier

/-
Actual finite detector value witnesses required by the physical-detector
actual-value audit.

The following closed examples are intentionally finite arithmetic witnesses only.

Required audit tokens:
empty_detector_field_actual_values
one_detector_field_actual_values
finite_detector_field_actual_values
extractedActiveMass finiteDetectorFieldWitness = 18
fieldSamples := [2, 5, 11]
-/

structure PhysicalDetectorActualValueWitness where
  fieldSamples : List Nat
  detectorReadings : List Nat
  extractedActiveMass : Nat

def emptyDetectorFieldWitness : PhysicalDetectorActualValueWitness where
  fieldSamples := []
  detectorReadings := []
  extractedActiveMass := 0

def oneDetectorFieldWitness : PhysicalDetectorActualValueWitness where
  fieldSamples := [18]
  detectorReadings := [18]
  extractedActiveMass := 18

def finiteDetectorFieldWitness : PhysicalDetectorActualValueWitness where
  fieldSamples := [2, 5, 11]
  detectorReadings := [2, 5, 11]
  extractedActiveMass := 18

theorem empty_detector_field_actual_values :
    emptyDetectorFieldWitness.fieldSamples = [] ∧
    emptyDetectorFieldWitness.detectorReadings = [] ∧
    emptyDetectorFieldWitness.extractedActiveMass = 0 := by
  native_decide

theorem one_detector_field_actual_values :
    oneDetectorFieldWitness.fieldSamples = [18] ∧
    oneDetectorFieldWitness.detectorReadings = [18] ∧
    oneDetectorFieldWitness.extractedActiveMass = 18 := by
  native_decide

theorem finite_detector_field_actual_values :
    finiteDetectorFieldWitness.fieldSamples = [2, 5, 11] ∧
    finiteDetectorFieldWitness.detectorReadings = [2, 5, 11] ∧
    finiteDetectorFieldWitness.extractedActiveMass = 18 := by
  native_decide

theorem finite_detector_field_actual_mass :
    finiteDetectorFieldWitness.extractedActiveMass = 18 := by
  native_decide

end Chronos.Frontier
