namespace Chronos
namespace Frontier

/--
A finite physical field sample.

This is deliberately finite and arithmetic-only: it is not a continuum
Einstein-matter field, not a PDE solution, and not an empirical observation.
-/
structure PhysicalEnergySample where
  detectorId : Nat
  radius : Nat
  energy : Nat
deriving DecidableEq, Repr

/--
Finite compact-support physical field data.

Compact support is represented by an explicit finite list of samples.
Energy nonnegativity is built in by using `Nat`.
-/
structure PhysicalFieldData where
  samples : List PhysicalEnergySample
deriving Repr

def PhysicalFieldData.supportSize (data : PhysicalFieldData) : Nat :=
  data.samples.length

def PhysicalFieldData.totalEnergy (data : PhysicalFieldData) : Nat :=
  data.samples.foldl (fun acc sample => acc + sample.energy) 0

theorem physicalFieldData_support_finite
  (data : PhysicalFieldData) :
  ∃ n : Nat, data.supportSize = n := by
  exact ⟨data.samples.length, rfl⟩

theorem physicalFieldData_totalEnergy_nonnegative
  (data : PhysicalFieldData) :
  0 ≤ data.totalEnergy := by
  exact Nat.zero_le _

theorem physicalFieldData_empty_totalEnergy_zero :
  ({ samples := [] } : PhysicalFieldData).totalEnergy = 0 := by
  rfl

end Frontier
end Chronos
