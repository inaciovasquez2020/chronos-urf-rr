import Chronos.Frontier.ExtractPhysicalDetectorWitness

namespace Chronos
namespace Frontier

/--
Finite detector-budget compatibility certificate.

This certifies only that the finite extracted detector witness agrees with the
finite physical field data and finite detector partition at the arithmetic
accounting layer.  It is not the detector-budget-to-gate theorem and does not
assert continuum physical correctness.
-/
structure DetectorBudgetCompatible
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) where
  activeMassMatchesTotalEnergy :
    (extractPhysicalDetectorWitness partition).activeMass = data.totalEnergy
  sampleCountMatchesSupportSize :
    (extractPhysicalDetectorWitness partition).sampleCount = data.supportSize
  detectorCellCountMatchesPartition :
    (extractPhysicalDetectorWitness partition).detectorCellCount = partition.cellCount
  activeDetectorIdsLengthMatchesDetectorCellCount :
    (extractPhysicalDetectorWitness partition).activeDetectorIds.length =
      (extractPhysicalDetectorWitness partition).detectorCellCount

theorem detectorBudgetCompatible_from_extractedWitness
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  DetectorBudgetCompatible partition := by
  exact {
    activeMassMatchesTotalEnergy :=
      extractPhysicalDetectorWitness_activeMass_eq_totalEnergy partition
    sampleCountMatchesSupportSize :=
      extractPhysicalDetectorWitness_sampleCount_eq_supportSize partition
    detectorCellCountMatchesPartition :=
      extractPhysicalDetectorWitness_detectorCellCount_eq_partitionCellCount partition
    activeDetectorIdsLengthMatchesDetectorCellCount :=
      extractPhysicalDetectorWitness_activeDetectorIds_length_eq_detectorCellCount partition
  }

theorem detectorBudgetCompatible_activeMass_eq_totalEnergy
  {data : PhysicalFieldData}
  {partition : FiniteDetectorPartition data}
  (h : DetectorBudgetCompatible partition) :
  (extractPhysicalDetectorWitness partition).activeMass = data.totalEnergy :=
  h.activeMassMatchesTotalEnergy

theorem detectorBudgetCompatible_sampleCount_eq_supportSize
  {data : PhysicalFieldData}
  {partition : FiniteDetectorPartition data}
  (h : DetectorBudgetCompatible partition) :
  (extractPhysicalDetectorWitness partition).sampleCount = data.supportSize :=
  h.sampleCountMatchesSupportSize

theorem detectorBudgetCompatible_detectorCellCount_eq_partitionCellCount
  {data : PhysicalFieldData}
  {partition : FiniteDetectorPartition data}
  (h : DetectorBudgetCompatible partition) :
  (extractPhysicalDetectorWitness partition).detectorCellCount = partition.cellCount :=
  h.detectorCellCountMatchesPartition

theorem detectorBudgetCompatible_activeMass_nonnegative
  {data : PhysicalFieldData}
  {partition : FiniteDetectorPartition data}
  (h : DetectorBudgetCompatible partition) :
  0 ≤ (extractPhysicalDetectorWitness partition).activeMass := by
  rw [h.activeMassMatchesTotalEnergy]
  exact physicalFieldData_totalEnergy_nonnegative data

theorem detectorBudgetCompatible_activeDetectorIds_length_eq_cellCount
  {data : PhysicalFieldData}
  {partition : FiniteDetectorPartition data}
  (h : DetectorBudgetCompatible partition) :
  (extractPhysicalDetectorWitness partition).activeDetectorIds.length =
    partition.cellCount := by
  rw [
    h.activeDetectorIdsLengthMatchesDetectorCellCount,
    h.detectorCellCountMatchesPartition,
  ]

theorem detectorBudgetCompatible_emptyData_activeMass_zero
  {partition : FiniteDetectorPartition ({ samples := [] } : PhysicalFieldData)}
  (h : DetectorBudgetCompatible partition) :
  (extractPhysicalDetectorWitness partition).activeMass = 0 := by
  rw [h.activeMassMatchesTotalEnergy]
  rfl

end Frontier
end Chronos
