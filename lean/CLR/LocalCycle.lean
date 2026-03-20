import Mathlib.Data.Fintype.Basic
import Mathlib.Data.ZMod.Basic

universe u

structure LocalCycleData where
  V : Type u
  [fV : Fintype V]
  [dV : DecidableEq V]
  edge : V → V → Prop
  [decEdge : DecidableRel edge]

attribute [instance] LocalCycleData.fV LocalCycleData.dV LocalCycleData.decEdge

def cycleVec (X : LocalCycleData) := X.V → ZMod 2

def local_cycle_equiv (X : LocalCycleData) (x y : cycleVec X) : Prop :=
  x = y

instance localCycleSetoid (X : LocalCycleData) : Setoid (cycleVec X) where
  r := local_cycle_equiv X
  iseqv := ⟨by intro x; rfl,
             by intro x y h; simpa [local_cycle_equiv] using h.symm,
             by intro x y z h1 h2; simpa [local_cycle_equiv] using h1.trans h2⟩

def LocalCycleQuot (X : LocalCycleData) := Quotient (localCycleSetoid X)
