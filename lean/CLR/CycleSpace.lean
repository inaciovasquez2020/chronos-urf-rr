import CLR.FiniteGraph
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.LinearAlgebra.FiniteDimensional

universe u

open Matrix FiniteGraph

namespace CLR

def orientedPairs (G : FiniteGraph) : Finset (G.V × G.V) := G.edgeSet

def edgeVec (G : FiniteGraph) := (G.V × G.V) → ZMod 2
def vertexVec (G : FiniteGraph) := G.V → ZMod 2

def incidence (G : FiniteGraph) : edgeVec G →ₗ[ZMod 2] vertexVec G where
  toFun x v := ∑ e in orientedPairs G, if e.1 = v ∨ e.2 = v then x e else 0
  map_add' x y := by
    ext v
    simp [Finset.sum_add_distrib, add_comm, add_left_comm, add_assoc]
  map_smul' a x := by
    ext v
    simp

def cycleSpace (G : FiniteGraph) : Submodule (ZMod 2) (edgeVec G) :=
  LinearMap.ker (incidence G)

noncomputable def cycleRank (G : FiniteGraph) : Nat :=
  FiniteDimensional.finrank (ZMod 2) (cycleSpace G)

end CLR
