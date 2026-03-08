import Oblivion.Rigidity.GraphBasics

namespace Oblivion

structure CycleTuple (G : Graph) where
  verts : List G.V

def IsSimpleCycle (G : Graph) (c : CycleTuple G) : Prop :=
  True

def CycleLength (c : CycleTuple G) : Nat :=
  c.verts.length

end Oblivion
