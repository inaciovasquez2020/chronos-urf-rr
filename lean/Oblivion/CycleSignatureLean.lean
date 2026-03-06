import Mathlib.Data.Finset.Basic

namespace Oblivion

universe u
variable {V : Type u} [DecidableEq V]

def cycleSignature (cycles : Finset (Finset V)) (v : V) : Finset (Finset V) :=
  cycles.filter (fun C => v ∈ C)

theorem cycleSignature_card_le (cycles : Finset (Finset V)) (v : V) :
  (cycleSignature cycles v).card ≤ cycles.card := by
  simpa [cycleSignature] using Finset.card_filter_le (s := cycles) (p := fun C => v ∈ C)

end Oblivion
