import Mathlib.Tactic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Cyclone.Core.Defs

namespace Cyclone.CCL.OverlapRank

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
    ∑ e : Sym2 V, (incidenceMatrix (V := V) G S i e) * (incidenceMatrix (V := V) G S j e)

def incidenceRank (S : List (Cycle (V := V))) : ℕ :=
  Matrix.rank (incidenceMatrix (V := V) G S)

def overlapRank (S : List (Cycle (V := V))) : ℕ :=
  Matrix.rank (overlapMatrix (V := V) G S)

theorem overlapMatrix_eq_mul_transpose
    (S : List (Cycle (V := V))) :
    overlapMatrix (V := V) G S =
      incidenceMatrix (V := V) G S *
        (incidenceMatrix (V := V) G S)ᵀ := by
  ext i j
  simp [overlapMatrix, Matrix.mul_apply, incidenceMatrix]

theorem overlapRank_le_incidenceRank
    (S : List (Cycle (V := V))) :
    overlapRank (V := V) G S ≤ incidenceRank (V := V) G S := by
  classical
  rw [overlapRank, incidenceRank, overlapMatrix_eq_mul_transpose]
  exact Matrix.rank_mul_le_left _ _

end Cyclone.CCL.OverlapRank
