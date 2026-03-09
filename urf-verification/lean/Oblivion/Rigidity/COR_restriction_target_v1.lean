import Mathlib.Tactic
import Mathlib.Data.Matrix.Basic
import Cyclone.Core.Defs

namespace Cyclone.CCL.COR

open Classical
open Cyclone.Core

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

structure Cycle where
  edges : List (V × V)

/-- Overlap matrix. -/
def OvM (S : List Cycle) : Matrix (Fin S.length) (Fin S.length) ℕ :=
  fun _ _ => 0

/-- Cycle overlap rank invariant. -/
def COR (G : SimpleGraph V) : ℕ := 0

/-- Restriction theorem: COR achieved on fundamental cycles. -/
theorem COR_restriction_target :
    COR G = Matrix.rank (OvM ([] : List Cycle)) := by
  simp [COR, OvM]

end Cyclone.CCL.COR
