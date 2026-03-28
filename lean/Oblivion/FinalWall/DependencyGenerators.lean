import Mathlib.Data.Finsupp.Basic
import Mathlib.LinearAlgebra.Basic

abbrev F2 := ZMod 2

-- Row index type (constraints)
variable {m n : ℕ}

-- Generator from a cycle in overlap graph (as a list of row indices)
def depGen (γ : List (Fin m)) : (Fin m →₀ F2) :=
  γ.foldl (fun acc i => acc + Finsupp.single i 1) 0

-- Support
def supp (w : Fin m →₀ F2) : Finset (Fin m) :=
  w.support

-- Placeholder: membership in left-kernel (row dependencies)
def isRowDep (A : Matrix (Fin m) (Fin n) F2) (w : Fin m →₀ F2) : Prop :=
  (Matrix.mulVec (Matrix.transpose A) w.toFun) = 0

-- Axiom to be discharged: cycles yield dependencies
axiom depGen_isRowDep
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : List (Fin m)) :
  isRowDep A (depGen γ)
