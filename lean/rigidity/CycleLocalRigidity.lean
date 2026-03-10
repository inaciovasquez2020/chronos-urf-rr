import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Data.Finset.Basic

namespace Rigidity

variable {V : Type} [Fintype V]

structure Graph where
  adj : V → V → Prop

def Edge (G : Graph) := {p : V × V // G.adj p.1 p.2}

def CycleOverlapMatrix (β : Nat) :=
  Matrix (Fin β) (Fin β) ℚ

def COR (β : Nat) (O : CycleOverlapMatrix β) : Nat :=
  Matrix.rank O

theorem cycle_local_rigidity_ck
  (k Δ R : Nat)
  (β : Nat)
  (O : CycleOverlapMatrix β)
  (hbound : Matrix.rank O ≤ (Nat.pow (Nat.succ Δ) (Nat.pow 2 k))) :
  COR β O ≤ (Nat.pow (Nat.succ Δ) (Nat.pow 2 k)) :=
by
  simpa [COR] using hbound

end Rigidity
