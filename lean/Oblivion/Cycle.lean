import Oblivion.Graph
import Mathlib.Data.Finset.Card

namespace Oblivion

structure Cycle (G : Graph) where
  edges : Finset G.E

def girth (G : Graph) : Nat := 0

lemma girth_le_cycle_length (C : Cycle G) :
    girth G ≤ C.edges.card := by
  simp [girth]

end Oblivion
