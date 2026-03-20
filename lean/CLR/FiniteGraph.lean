import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.LinearAlgebra.FiniteDimensional

universe u

structure FiniteGraph where
  V : Type u
  instFintypeV : Fintype V
  instDecidableEqV : DecidableEq V
  adj : V → V → Prop
  instDecidableRelAdj : DecidableRel adj
  symm : Symmetric adj
  loopless : Irreflexive adj

attribute [instance] FiniteGraph.instFintypeV
attribute [instance] FiniteGraph.instDecidableEqV
attribute [instance] FiniteGraph.instDecidableRelAdj

namespace FiniteGraph

def edgeSet (G : FiniteGraph) : Finset (G.V × G.V) :=
  Finset.univ.filter (fun e => G.adj e.1 e.2)

def adjMatrix (G : FiniteGraph) : Matrix G.V G.V (ZMod 2) :=
  fun i j => if G.adj i j then 1 else 0

end FiniteGraph
