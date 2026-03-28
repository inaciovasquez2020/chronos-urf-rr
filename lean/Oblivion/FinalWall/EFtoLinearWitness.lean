import Mathlib.Data.Finsupp.Basic
import Mathlib.LinearAlgebra.Basic
import Mathlib.Data.Matrix.Basic

abbrev F2 := ZMod 2

open Finsupp

variable {m n : ℕ}

structure EFType where
  id : ℕ
deriving DecidableEq

variable (constraintsOf : EFType → Finset (Fin m))

def Phi (τ : EFType) : (Fin m →₀ F2) :=
  ∑ i in constraintsOf τ, single i 1

def witnessVector (τ₀ τ₁ : EFType) : (Fin m →₀ F2) :=
  Phi constraintsOf τ₀ + Phi constraintsOf τ₁

def boundedSupportLog (w : Fin m →₀ F2) : Prop :=
  w.support.card ≤ Nat.log (m + 2)

def rowRealizable (A : Matrix (Fin m) (Fin n) F2) (w : Fin m →₀ F2) : Prop :=
  ∃ u : Fin n → F2, Matrix.mulVec (Matrix.transpose A) w.toFun = u

theorem EF_separation_reduces_to_constraint_difference
  (τ₀ τ₁ : EFType)
  (h : τ₀ ≠ τ₁) :
  witnessVector constraintsOf τ₀ τ₁ ≠ 0 := by
  classical
  intro hz
  have : Phi constraintsOf τ₀ = Phi constraintsOf τ₁ := by
    simpa [witnessVector, add_eq_zero_iff_eq] using hz
  exact h <| by cases τ₀; cases τ₁; cases this; rfl

