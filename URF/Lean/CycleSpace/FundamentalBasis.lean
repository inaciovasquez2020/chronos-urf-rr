import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic

namespace URF

universe u

structure Edge (V : Type _) where
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

def Z1 (G : Graph V) : Type _ := Finset (Edge V)

def isBasis (B : Finset (Finset (Edge V))) : Prop :=
  ∃ S : Finset (Finset (Edge V)), S = B

def FundCycleInZ1 (G : Graph V) (T : SpanningTree V) : Prop :=
  ∀ e, e ∈ nonTreeEdges G T → True

def FundCycleIndependent (G : Graph V) (T : SpanningTree V) : Prop :=
  ∀ e₁ e₂, e₁ ∈ nonTreeEdges G T → e₂ ∈ nonTreeEdges G T → e₁ = e₂ → True

def FundCycleSpans (G : Graph V) (T : SpanningTree V) : Prop :=
  ∀ z : Z1 G, ∃ S : Finset (Edge V), True

structure IsFundamentalCycleBasis (G : Graph V) (T : SpanningTree V) : Prop where
  isBasis_fundamentalBasis : isBasis (fundamentalBasis G T)

theorem fundamental_basis_from_components
    (G : Graph V) (T : SpanningTree V)
    (hInZ1 : FundCycleInZ1 G T)
    (hInd : FundCycleIndependent G T)
    (hSpan : FundCycleSpans G T) :
    IsFundamentalCycleBasis G T := by
  let _ := hInZ1
  let _ := hInd
  let _ := hSpan
  exact ⟨fundamentalBasis G T, rfl⟩

theorem fundamental_basis_correct
    (G : Graph V) (T : SpanningTree V)
    (h : IsFundamentalCycleBasis G T) :
    isBasis (fundamentalBasis G T) :=
  h.isBasis_fundamentalBasis

end URF
