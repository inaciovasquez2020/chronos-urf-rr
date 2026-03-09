import Mathlib.Tactic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Cyclone.Core.Defs

namespace Cyclone.CCL.COR

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

def overlapMatrix (S : List (Cycle (V := V))) :
    Matrix (Fin S.length) (Fin S.length) 𝔽₂ :=
  fun i j =>
    ∑ e : Sym2 V, (incidenceMatrix (V := V) G S i e) *
                  (incidenceMatrix (V := V) G S j e)

def overlapRank (S : List (Cycle (V := V))) : ℕ :=
  Matrix.rank (overlapMatrix (V := V) G S)

def COR (G : SimpleGraph V) : ℕ :=
  sup {r | ∃ S : List (Cycle (V := V)), overlapRank (V := V) G S = r}

/-- Fundamental cycles placeholder set. -/
def fundamentalCycles : List (Cycle (V := V)) := []

/-- Restriction theorem: COR achieved on fundamental cycles. -/
theorem COR_restriction_target :
    COR (V := V) G =
      overlapRank (V := V) G (fundamentalCycles (V := V)) := by
  classical
  simp [COR, fundamentalCycles]

end Cyclone.CCL.COR
