import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Algebra.BigOperators.Basic
import Mathlib.Data.Finsupp.Basic

abbrev F2 := ZMod 2

open BigOperators

variable {m n : ℕ}

def depGen (γ : Finset (Fin m)) : (Fin m →₀ F2) :=
  ∑ i in γ, Finsupp.single i 1

def isRowDep (A : Matrix (Fin m) (Fin n) F2) (w : Fin m →₀ F2) : Prop :=
  Matrix.mulVec (Matrix.transpose A) w.toFun = 0

def zeroColumnSum (A : Matrix (Fin m) (Fin n) F2) (γ : Finset (Fin m)) : Prop :=
  ∀ j : Fin n, ∑ i in γ, A i j = 0

theorem depGen_isRowDep
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : zeroColumnSum A γ) :
  isRowDep A (depGen γ) := by
  classical
  ext j
  unfold isRowDep depGen
  simp [Matrix.mulVec, Matrix.dotProduct, Finset.sum_comm, hγ j]
