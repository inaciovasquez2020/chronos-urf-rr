import Oblivion.Rigidity.GraphBasics

namespace Oblivion

structure CycleTuple (G : Graph) where
  verts : List G.V

def CycleLength (c : CycleTuple G) : Nat :=
  c.verts.length

def IsSimpleCycle (G : Graph) (c : CycleTuple G) : Prop :=
  c.verts.length ≥ 3

theorem cycle_length_nonneg
  (G : Graph) (c : CycleTuple G) :
  0 ≤ CycleLength c :=
by
  simp [CycleLength]

theorem simple_cycle_has_length
  (G : Graph) (c : CycleTuple G)
  (h : IsSimpleCycle G c) :
  CycleLength c ≥ 3 :=
by
  simpa [IsSimpleCycle, CycleLength] using h

end Oblivion
