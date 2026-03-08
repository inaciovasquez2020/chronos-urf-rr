import Oblivion.Rigidity.GraphBasics
import Oblivion.Rigidity.CycleStructures

namespace Oblivion

def EdgeSet (G : Graph) : Type := Nat

structure CycleIncidenceMatrix (G : Graph) (R : Nat) where
  rows : Nat
  cols : Nat

def RankF2 (M : CycleIncidenceMatrix G R) : Nat :=
  0

end Oblivion
