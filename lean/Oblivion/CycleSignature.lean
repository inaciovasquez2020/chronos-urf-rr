import Mathlib.Data.Finset

namespace Oblivion

variable {V : Type} [DecidableEq V]

def cycleSignature (cycles : Finset (Finset V)) (v : V) : Finset Nat :=
cycles.filter (fun C => v ∈ C) |>.image (fun _ => 1)

theorem signature_bound
(cycles : Finset (Finset V))
(v : V) :
(cycleSignature cycles v).card ≤ cycles.card := by
  simp [cycleSignature]

end Oblivion
