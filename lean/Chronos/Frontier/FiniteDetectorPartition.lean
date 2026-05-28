import Chronos.Frontier.PhysicalFieldDataFiniteSamples

namespace Chronos
namespace Frontier

/--
A finite detector cell.

This is an arithmetic detector cell only.  It is not a continuum detector,
not a PDE domain, and not an empirical instrument model.
-/
structure DetectorCell where
  detectorId : Nat
  innerRadius : Nat
  outerRadius : Nat
deriving DecidableEq, Repr

def DetectorCell.width (cell : DetectorCell) : Nat :=
  cell.outerRadius - cell.innerRadius

theorem detectorCell_width_nonnegative
  (cell : DetectorCell) :
  0 ≤ cell.width := by
  exact Nat.zero_le _

/--
A finite detector partition over finite physical field data.

The partition is represented by an explicit finite list of detector cells.
No coverage, disjointness, geometry, or physical extraction theorem is asserted here.
-/
structure FiniteDetectorPartition (data : PhysicalFieldData) where
  cells : List DetectorCell
deriving Repr

def FiniteDetectorPartition.cellCount
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) : Nat :=
  partition.cells.length

def FiniteDetectorPartition.activeCellIds
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) : List Nat :=
  partition.cells.map (fun cell => cell.detectorId)

theorem finiteDetectorPartition_cells_finite
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  ∃ n : Nat, partition.cellCount = n := by
  exact ⟨partition.cells.length, rfl⟩

theorem finiteDetectorPartition_empty_cellCount_zero
  (data : PhysicalFieldData) :
  ({ cells := [] } : FiniteDetectorPartition data).cellCount = 0 := by
  rfl

theorem finiteDetectorPartition_activeCellIds_finite
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  ∃ n : Nat, partition.activeCellIds.length = n := by
  exact ⟨partition.cells.length, by simp [FiniteDetectorPartition.activeCellIds]⟩

theorem finiteDetectorPartition_activeCellIds_length_eq_cellCount
  {data : PhysicalFieldData}
  (partition : FiniteDetectorPartition data) :
  partition.activeCellIds.length = partition.cellCount := by
  simp [
    FiniteDetectorPartition.activeCellIds,
    FiniteDetectorPartition.cellCount,
  ]

end Frontier
end Chronos
