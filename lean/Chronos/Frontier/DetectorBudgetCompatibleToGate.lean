import Chronos.Frontier.DetectorBudgetCompatible

namespace Chronos
namespace Frontier

/--
Restricted finite-detector extraction-gate certificate derived from detector-budget
compatibility.

This is a finite arithmetic gate certificate only.  It records exactly the
finite consequences needed from `DetectorBudgetCompatible`: nonnegative extracted
active mass, agreement of detector ids with partition cells, agreement of sample
count with field-data support, and agreement of detector-cell count with the
partition.

It does not assert coverage, disjointness, geometric correctness, empirical
detector correctness, or any continuum PDE/gravity theorem.
-/
structure RestrictedFiniteDetectorExtractionGateFromBudget
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) where
  compatibilityCertificate :
    DetectorBudgetCompatible partition
  activeMassNonnegative :
    0 ≤ (extractPhysicalDetectorWitness partition).activeMass
  activeDetectorIdsLengthMatchesCellCount :
    (extractPhysicalDetectorWitness partition).activeDetectorIds.length =
      partition.cellCount
  sampleCountMatchesSupportSize :
    (extractPhysicalDetectorWitness partition).sampleCount =
      data.supportSize
  detectorCellCountMatchesPartition :
    (extractPhysicalDetectorWitness partition).detectorCellCount =
      partition.cellCount

theorem detectorBudgetCompatible_to_restrictedFiniteDetectorExtractionGate
  {data : PhysicalFieldData}
  {partition : FiniteDetectorPartition data}
  (h : DetectorBudgetCompatible partition) :
  RestrictedFiniteDetectorExtractionGateFromBudget partition := by
  exact {
    compatibilityCertificate := h
    activeMassNonnegative :=
      detectorBudgetCompatible_activeMass_nonnegative h
    activeDetectorIdsLengthMatchesCellCount :=
      detectorBudgetCompatible_activeDetectorIds_length_eq_cellCount h
    sampleCountMatchesSupportSize :=
      detectorBudgetCompatible_sampleCount_eq_supportSize h
    detectorCellCountMatchesPartition :=
      detectorBudgetCompatible_detectorCellCount_eq_partitionCellCount h
  }

theorem restrictedFiniteDetectorExtractionGate_from_extractedWitness
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  RestrictedFiniteDetectorExtractionGateFromBudget partition := by
  exact detectorBudgetCompatible_to_restrictedFiniteDetectorExtractionGate
    (detectorBudgetCompatible_from_extractedWitness partition)

theorem restrictedFiniteDetectorExtractionGate_activeMass_nonnegative
  {data : PhysicalFieldData}
  {partition : FiniteDetectorPartition data}
  (gate : RestrictedFiniteDetectorExtractionGateFromBudget partition) :
  0 ≤ (extractPhysicalDetectorWitness partition).activeMass :=
  gate.activeMassNonnegative

theorem restrictedFiniteDetectorExtractionGate_activeDetectorIds_length_eq_cellCount
  {data : PhysicalFieldData}
  {partition : FiniteDetectorPartition data}
  (gate : RestrictedFiniteDetectorExtractionGateFromBudget partition) :
  (extractPhysicalDetectorWitness partition).activeDetectorIds.length =
    partition.cellCount :=
  gate.activeDetectorIdsLengthMatchesCellCount

theorem restrictedFiniteDetectorExtractionGate_sampleCount_eq_supportSize
  {data : PhysicalFieldData}
  {partition : FiniteDetectorPartition data}
  (gate : RestrictedFiniteDetectorExtractionGateFromBudget partition) :
  (extractPhysicalDetectorWitness partition).sampleCount =
    data.supportSize :=
  gate.sampleCountMatchesSupportSize

theorem restrictedFiniteDetectorExtractionGate_detectorCellCount_eq_partitionCellCount
  {data : PhysicalFieldData}
  {partition : FiniteDetectorPartition data}
  (gate : RestrictedFiniteDetectorExtractionGateFromBudget partition) :
  (extractPhysicalDetectorWitness partition).detectorCellCount =
    partition.cellCount :=
  gate.detectorCellCountMatchesPartition

theorem restrictedFiniteDetectorExtractionGate_emptyData_activeMass_zero
  {partition : FiniteDetectorPartition ({ samples := [] } : PhysicalFieldData)}
  (gate : RestrictedFiniteDetectorExtractionGateFromBudget partition) :
  (extractPhysicalDetectorWitness partition).activeMass = 0 := by
  exact detectorBudgetCompatible_emptyData_activeMass_zero
    gate.compatibilityCertificate

end Frontier
end Chronos
