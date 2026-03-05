import Mathlib.Data.Finset.Basic

namespace Oblivion

variable {V : Type} [DecidableEq V]

def cycleSignature (cycles : Finset (Finset V)) (v : V) : Finset (Finset V) :=
cycles.filter (fun C => v ∈ C)

theorem signature_finite
(cycles : Finset (Finset V)) (v : V) :
(cycleSignature cycles v).card ≤ cycles.card := by
simp [cycleSignature]

end Oblivion
