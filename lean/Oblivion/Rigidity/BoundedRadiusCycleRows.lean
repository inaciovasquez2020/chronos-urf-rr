import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Sym.Sym2
import Mathlib.Data.Finset.Basic
import Mathlib.Data.ZMod.Basic
import Oblivion.Rigidity.FiniteGraphModel
import Oblivion.Rigidity.CycleRowSpace
import Oblivion.Rigidity.NeighborhoodBalls

namespace Oblivion

universe u

abbrev GraphEdge (V : Type u) := Sym2 V

structure GraphCycle {V : Type u} [DecidableEq V] (G : SimpleGraph V) where
  edges : Finset (GraphEdge V)

def cycleContainedInBall {V : Type u} [DecidableEq V]
    (G : SimpleGraph V) (v : V) (R : Nat) (C : GraphCycle G) : Prop :=
  ∀ e ∈ C.edges, ∃ x y : V, Quot.mk _ (x, y) = e ∧ x ∈ ballSet G v R ∧ y ∈ ballSet G v R

def boundedRadiusCycleFamily {V : Type u} [DecidableEq V]
    (G : SimpleGraph V) (R : Nat) := Σ v : V, {C : GraphCycle G // cycleContainedInBall G v R C}

def boundedRadiusCycleSupport {V : Type u} [DecidableEq V]
    {G : SimpleGraph V} {R : Nat} (i : boundedRadiusCycleFamily G R) : CycleSupport V :=
  ⟨i.2.1.edges⟩

def boundedRadiusCycleRows {V : Type u} [DecidableEq V]
    {G : SimpleGraph V} {R : Nat} :
    boundedRadiusCycleFamily G R → Edge V → ZMod 2 :=
  fun i => (boundedRadiusCycleSupport i).row

end Oblivion
