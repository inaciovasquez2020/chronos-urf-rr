import Mathlib.Tactic
import Mathlib.Data.Fintype.Basic
import Cyclone.Core.Defs

namespace Cyclone.CCL.CCL4

open Classical
open Cyclone.Core

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]
variable (root : V)
variable (R : ℕ)

/-- Fundamental cycle constructed from a BFS tree edge. -/
structure FundamentalCycle where
  edge : V × V
  path_u_root : List V
  path_root_v : List V

/-- Length of a fundamental cycle. -/
def cycleLength (C : FundamentalCycle) : ℕ :=
  C.path_u_root.length + C.path_root_v.length + 1

/-- Locality lemma: fundamental cycle length bound. -/
theorem fundamental_cycle_length_bound
    (C : FundamentalCycle)
    (h1 : C.path_u_root.length ≤ R)
    (h2 : C.path_root_v.length ≤ R) :
    cycleLength C ≤ 2*R + 1 := by
  unfold cycleLength
  have hsum : C.path_u_root.length + C.path_root_v.length ≤ 2*R := by
    exact Nat.add_le_add h1 h2
  have := Nat.succ_le_succ hsum
  simpa [two_mul, Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc] using this

end Cyclone.CCL.CCL4
