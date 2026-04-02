import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.LinearAlgebra.FiniteDimensional

abbrev F2 := ZMod 2

variable {m n : ℕ}

def depFamily (m : ℕ) := Fin m → (Fin m →₀ F2)

def depFamilyIndependent (W : depFamily m) : Prop :=
  LinearIndependent F2 W

def rankCompressionTarget (A : Matrix (Fin m) (Fin n) F2) (d : ℕ) : Prop :=
  ∃ W : depFamily d,
    depFamilyIndependent W ∧
    Matrix.rank A ≤ n - d

theorem rank_compression_from_independent_dependencies
  (A : Matrix (Fin m) (Fin n) F2)
  (d : ℕ)
  (h : ∃ W : depFamily d, depFamilyIndependent W) :
  rankCompressionTarget A d := by
  rcases h with ⟨W,hW⟩
  refine ⟨W,hW,?_⟩
  omega

