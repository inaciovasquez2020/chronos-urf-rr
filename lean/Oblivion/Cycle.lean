import Oblivion.Graph

namespace Oblivion

structure Cycle (G : Graph) where
  edges : Finset G.E

def girth (G : Graph) : Nat := 0

lemma girth_le_cycle_length (C : Cycle G) :
    girth G ≤ C.edges.card := by
  admit

end Oblivion
