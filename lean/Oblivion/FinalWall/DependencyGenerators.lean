import Mathlib.Data.Finsupp.Basic
import Mathlib.LinearAlgebra.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.BigOperators.Basic

abbrev F2 := ZMod 2

open Finsupp
open BigOperators

variable {m n : ℕ}

def depGen (γ : Finset (Fin m)) : (Fin m →₀ F2) :=
  ∑ i in γ, single i 1

def isRowDep (A : Matrix (Fin m) (Fin n) F2) (w : Fin m →₀ F2) : Prop :=
  Matrix.mulVec (Matrix.transpose A) w.toFun = 0

def zeroColumnSum (A : Matrix (Fin m) (Fin n) F2) (γ : Finset (Fin m)) : Prop :=
  ∀ j : Fin n, ∑ i in γ, A i j = 0

lemma parity_to_ZMod2_zero
  {s : Finset α} [DecidableEq α] (f : α → F2)
  (h : ∑ x in s, f x = 0) :
  ∑ x in s, f x = 0 := h

theorem depGen_isRowDep
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : zeroColumnSum A γ) :
  isRowDep A (depGen γ) := by
  classical
  ext j
  simp [isRowDep, depGen, Matrix.mulVec, hγ j, Finset.sum_comm, Finset.sum_sigma']
