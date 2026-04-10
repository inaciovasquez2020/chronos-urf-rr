import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.BigOperators.Basic
import Mathlib.LinearAlgebra.Basic

universe u

open BigOperators

namespace URF

structure EdgeData (V : Type u) where
  fst : V
  snd : V

structure FinGraph where
  V : Type u
  E : Type u
  instFintypeV : Fintype V
  instDecidableEqV : DecidableEq V
  instFintypeE : Fintype E
  instDecidableEqE : DecidableEq E
  inc : E → EdgeData V

attribute [instance] FinGraph.instFintypeV
attribute [instance] FinGraph.instDecidableEqV
attribute [instance] FinGraph.instFintypeE
attribute [instance] FinGraph.instDecidableEqE

def C1 (G : FinGraph) := G.E → ZMod 2
def C0 (G : FinGraph) := G.V → ZMod 2

def boundary (G : FinGraph) : C1 G → C0 G :=
  fun x v =>
    ∑ e in Finset.univ,
      if (G.inc e).fst = v ∨ (G.inc e).snd = v then x e else 0

def Z1 (G : FinGraph) : Submodule (ZMod 2) (C1 G) :=
  LinearMap.ker
    { toFun := boundary G
      map_add' := by
        intro x y
        funext v
        simp [boundary, Finset.sum_add_distrib]
      map_smul' := by
        intro a x
        funext v
        simp [boundary, Finset.mul_sum] }

end URF
