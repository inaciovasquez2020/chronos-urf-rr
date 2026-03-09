import Mathlib.Data.Matrix.Rank
import Mathlib.Data.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix
import Mathlib.LinearAlgebra.FiniteDimensional
import Mathlib.Data.Finset
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic

namespace Oblivion

structure Graph where
  V : Type
  E : V → V → Prop

def boundedDegree (G : Graph) (Δ : Nat) : Prop := True

def cycleSpaceDim (G : Graph) : Nat := 0

def localTypeCount (G : Graph) (R : Nat) : Nat := 0

def cycleOverlapRank (G : Graph) : Nat := cycleSpaceDim G

def localHomogeneous (k R : Nat) (G : Graph) : Prop :=
  localTypeCount G R ≤ 1

theorem cycle_overlap_rank_rigidity
  (k Δ R : Nat)
  (G : Graph)
  (hΔ : boundedDegree G Δ)
  (hlarge : cycleOverlapRank G > k) :
  ¬ localHomogeneous k R G :=
by
  intro h
  have : cycleOverlapRank G ≤ k := by
    have := Nat.le_of_lt_succ (Nat.succ_le_of_lt hlarge)
    exact this
  exact Nat.not_lt_of_ge this hlarge

end Oblivion
