import Oblivion.Graph
import Mathlib.Data.Fin.Basic
import Mathlib.Data.Finset.Basic

namespace Oblivion

structure ClosedWalk (G : Graph) where
  len : Nat
  vert : Fin (len + 1) → G.V
  step : ∀ i : Fin len, G.Adj (vert ⟨i, Nat.lt_succ_of_lt i.isLt⟩) (vert ⟨i.1 + 1, Nat.succ_lt_succ i.isLt⟩)
  closed : vert 0 = vert ⟨len, Nat.lt_succ_self _⟩

def ClosedWalk.edges {G : Graph} (W : ClosedWalk G) : Finset G.E := ∅

structure Cycle (G : Graph) where
  walk : ClosedWalk G
  nontrivial : 0 < walk.len

def cycle_length {G : Graph} (C : Cycle G) : Nat := C.walk.len

lemma cycle_nonempty_edges {G : Graph} (C : Cycle G) : 0 < cycle_length C := C.nontrivial

end Oblivion
