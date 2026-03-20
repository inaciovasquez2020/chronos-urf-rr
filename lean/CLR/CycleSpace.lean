import Lean.CLR.LocalCycle
import Mathlib.LinearAlgebra.FiniteDimensional
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Basic

universe u

open Classical

def cycleVec (X : LocalCycleData) := X.V → ZMod 2

def boundary (X : LocalCycleData) (v : X.V) : cycleVec X :=
  fun w => if X.edge v w then 1 else 0

def boundarySpan (X : LocalCycleData) : Submodule (ZMod 2) (cycleVec X) :=
  Submodule.span (ZMod 2) (Set.range (boundary X))

def local_cycle_equiv (X : LocalCycleData) (x y : cycleVec X) : Prop :=
  x - y ∈ boundarySpan X

instance localCycleSetoid (X : LocalCycleData) : Setoid (cycleVec X) where
  r := local_cycle_equiv X
  iseqv :=
  ⟨
    by
      intro x
      have : x - x = 0 := by simp
      simpa [local_cycle_equiv, this] using
        Submodule.zero_mem (boundarySpan X),
    by
      intro x y h
      have : y - x = -(x - y) := by simp
      have h' := Submodule.neg_mem (boundarySpan X) h
      simpa [local_cycle_equiv, this] using h',
    by
      intro x y z hxy hyz
      have : x - z = (x - y) + (y - z) := by
        ext v; simp [sub_eq_add_neg, add_comm, add_left_comm, add_assoc]
      have hsum :=
        Submodule.add_mem (boundarySpan X) hxy hyz
      simpa [local_cycle_equiv, this] using hsum
  ⟩

def LocalCycleQuot (X : LocalCycleData) :=
  Quotient (localCycleSetoid X)

def cycleSpace (X : LocalCycleData) :=
  (cycleVec X) ⧸ (boundarySpan X)

noncomputable def cycleRank (X : LocalCycleData) : Nat :=
  FiniteDimensional.finrank (ZMod 2) (cycleSpace X)

