import Mathlib.Data.Finsupp.Basic
import Mathlib.LinearAlgebra.Basic
import Mathlib.Data.Matrix.Basic

abbrev F2 := ZMod 2

open Finsupp

variable {m n : ℕ}

def depGen (γ : List (Fin m)) : (Fin m →₀ F2) :=
  γ.foldl (fun acc i => acc + single i 1) 0

def isRowDep (A : Matrix (Fin m) (Fin n) F2) (w : Fin m →₀ F2) : Prop :=
  Matrix.mulVec (Matrix.transpose A) w.toFun = 0

def rowSupport (A : Matrix (Fin m) (Fin n) F2) (i : Fin m) : Finset (Fin n) :=
  Finset.univ.filter (fun j => A i j ≠ 0)

def evenOnCommonSupport (A : Matrix (Fin m) (Fin n) F2) (γ : List (Fin m)) : Prop :=
  ∀ j : Fin n, Even (((γ.map fun i => if A i j = 0 then 0 else 1).sum))

theorem depGen_isRowDep
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : List (Fin m))
  (hγ : evenOnCommonSupport A γ) :
  isRowDep A (depGen γ) := by
  classical
  ext j
  unfold isRowDep depGen
  simp [Matrix.mulVec, hγ, Finset.sum_filter]

