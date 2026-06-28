import Mathlib.Data.Finset.Card

namespace Oblivion

variable {V : Type} [DecidableEq V]

def cycleSignature (cycles : Finset (Finset V)) (v : V) : Finset Nat :=
cycles.filter (fun C => v ∈ C) |>.image (fun _ => 1)

theorem signature_bound
(cycles : Finset (Finset V))
(v : V) :
(cycleSignature cycles v).card ≤ cycles.card := by
  unfold cycleSignature
  exact Nat.le_trans
    (Finset.card_image_le)
    (Finset.card_filter_le cycles (fun C => v ∈ C))

end Oblivion
