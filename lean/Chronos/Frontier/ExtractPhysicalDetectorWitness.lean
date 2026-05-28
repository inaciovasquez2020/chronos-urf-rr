import Chronos.Frontier.FiniteDetectorPartition

namespace Chronos
namespace Frontier

/--
Finite detector witness extracted from finite physical field data and a finite detector partition.

This is an arithmetic witness object only.  It records finite sampled mass,
finite sample support, finite detector-cell count, and finite active detector ids.
It is not a physical detector-field extraction theorem and does not assert budget
compatibility.
-/
structure ExtractedPhysicalDetectorWitness where
  activeMass : Nat
  sampleCount : Nat
  detectorCellCount : Nat
  activeDetectorIds : List Nat
deriving Repr

/--
Extract a finite arithmetic detector witness from finite field data and a finite
detector partition.

The active mass is the finite sampled total energy.  The detector ids are the
finite ids supplied by the partition.
-/
def extractPhysicalDetectorWitness
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  ExtractedPhysicalDetectorWitness :=
  {
    activeMass := data.totalEnergy
    sampleCount := data.supportSize
    detectorCellCount := partition.cellCount
    activeDetectorIds := partition.activeCellIds
  }

theorem extractPhysicalDetectorWitness_activeMass_eq_totalEnergy
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  (extractPhysicalDetectorWitness partition).activeMass = data.totalEnergy := by
  rfl

theorem extractPhysicalDetectorWitness_sampleCount_eq_supportSize
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  (extractPhysicalDetectorWitness partition).sampleCount = data.supportSize := by
  rfl

theorem extractPhysicalDetectorWitness_detectorCellCount_eq_partitionCellCount
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  (extractPhysicalDetectorWitness partition).detectorCellCount = partition.cellCount := by
  rfl

theorem extractPhysicalDetectorWitness_activeDetectorIds_eq_partitionIds
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  (extractPhysicalDetectorWitness partition).activeDetectorIds = partition.activeCellIds := by
  rfl

theorem extractPhysicalDetectorWitness_activeMass_nonnegative
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  0 ≤ (extractPhysicalDetectorWitness partition).activeMass := by
  exact Nat.zero_le _

theorem extractPhysicalDetectorWitness_activeDetectorIds_finite
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  ∃ n : Nat, (extractPhysicalDetectorWitness partition).activeDetectorIds.length = n := by
  exact ⟨partition.activeCellIds.length, rfl⟩

theorem extractPhysicalDetectorWitness_activeDetectorIds_length_eq_detectorCellCount
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  (extractPhysicalDetectorWitness partition).activeDetectorIds.length =
    (extractPhysicalDetectorWitness partition).detectorCellCount := by
  exact finiteDetectorPartition_activeCellIds_length_eq_cellCount partition

theorem extractPhysicalDetectorWitness_emptyData_activeMass_zero
  (partition : FiniteDetectorPartition ({ samples := [] } : PhysicalFieldData)) :
  (extractPhysicalDetectorWitness partition).activeMass = 0 := by
  rfl

end Frontier
end Chronos
