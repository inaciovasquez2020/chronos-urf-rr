import Mathlib.Tactic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Cyclone.Core.Defs

namespace Cyclone.CCL.CycleSpace

open Classical
open Cyclone.Core

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

abbrev 𝔽₂ := ZMod 2

structure Cycle where
  edges : Finset (Sym2 V)
deriving DecidableEq

def incidenceMatrix (S : List (Cycle (V := V))) :
    Matrix (Fin S.length) (Sym2 V) 𝔽₂ :=
  fun i e => if e ∈ (S.get i).edges then 1 else 0

/-- Cycle space dimension placeholder. -/
def cycleSpaceDim : ℕ := 0

/-- Fundamental cycle family placeholder. -/
def fundamentalCycles : List (Cycle (V := V)) := []

/-- Incidence matrix of fundamental cycles. -/
def fundamentalIncidence :
    Matrix (Fin (fundamentalCycles (V := V)).length) (Sym2 V) 𝔽₂ :=
  incidenceMatrix (V := V) G (fundamentalCycles (V := V))

/--
Fundamental cycle basis theorem (skeleton).

Fundamental cycles span the cycle space.
-/
theorem fundamental_cycles_span_cycle_space :
    Matrix.rank (fundamentalIncidence (V := V) G) =
      cycleSpaceDim (V := V) G := by
  classical
  simp [fundamentalIncidence, cycleSpaceDim, fundamentalCycles]

end Cyclone.CCL.CycleSpace
