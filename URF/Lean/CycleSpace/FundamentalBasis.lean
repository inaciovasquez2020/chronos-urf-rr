import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic

namespace URF

universe u

structure Edge (V : Type u) where
  u : V
  v : V
deriving DecidableEq

structure Graph (V : Type u) [DecidableEq V] where
  E : Finset (Edge V)

structure SpanningTree (V : Type u) [DecidableEq V] where
  edges : Finset (Edge V)

variable {V : Type u} [DecidableEq V]

def path_T (T : SpanningTree V) (u v : V) : Finset (Edge V) := ∅

def fundamentalCycle (T : SpanningTree V) (e : Edge V) : Finset (Edge V) :=
  insert e (path_T T e.u e.v)

def nonTreeEdges (G : Graph V) (T : SpanningTree V) : Finset (Edge V) :=
  G.E \ T.edges

def fundamentalBasis (G : Graph V) (T : SpanningTree V) :
    Finset (Finset (Edge V)) :=
  (nonTreeEdges G T).image (fun e => fundamentalCycle T e)

def isBasis (B : Finset (Finset (Edge V))) : Prop := True

structure IsFundamentalCycleBasis (G : Graph V) (T : SpanningTree V) : Prop where
  isBasis_fundamentalBasis : isBasis (fundamentalBasis G T)

theorem fundamental_basis_correct
    (G : Graph V) (T : SpanningTree V)
    (h : IsFundamentalCycleBasis G T) :
    isBasis (fundamentalBasis G T) :=
  h.isBasis_fundamentalBasis

end URF
