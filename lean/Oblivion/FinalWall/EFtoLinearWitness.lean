import Mathlib.Data.Finsupp.Basic
import Mathlib.LinearAlgebra.Basic

abbrev F2 := ZMod 2

variable {m n : ℕ}

-- Abstract EF-type and extraction interface
structure EFType where
  id : ℕ

-- Constraint selector from EF-type
constant constraintsOf : EFType → List (Fin m)

-- Linear encoding
def Phi (τ : EFType) : (Fin m →₀ F2) :=
  (constraintsOf τ).foldl (fun acc i => acc + Finsupp.single i 1) 0

-- Rowspace membership (placeholder)
def inRowspace (A : Matrix (Fin m) (Fin n) F2) (w : Fin m →₀ F2) : Prop :=
  ∃ (x : Fin n → F2), Matrix.mulVec (Matrix.transpose A) w.toFun = 0

-- Axiom: EF separation ⇒ rowspace witness with bounded support
axiom EF_separation_witness
  (A : Matrix (Fin m) (Fin n) F2)
  (τ₀ τ₁ : EFType) (h : τ₀ ≠ τ₁) :
  ∃ w, inRowspace A w ∧ w.support.card ≤ Nat.log (n+1)
