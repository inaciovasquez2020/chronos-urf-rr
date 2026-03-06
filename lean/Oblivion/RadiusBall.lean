import Mathlib.Data.Finset.Basic
import Mathlib.Data.Nat.Basic

namespace Oblivion

universe u
variable {V : Type u} [DecidableEq V]

structure Graph where
  Adj : V → V → Prop

-- Minimal placeholder distance predicate (to be replaced by Mathlib graph distance)
def Dist (G : Graph) (u v : V) : Nat := 0

def radiusBall (G : Graph) (v : V) (R : Nat) : Finset V :=
  Finset.univ.filter (fun u => Dist G v u ≤ R)

end Oblivion
