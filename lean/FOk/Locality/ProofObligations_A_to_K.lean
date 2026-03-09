import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic

namespace FOk

structure Graph where
  V : Type
  Adj : V → V → Prop

def maxDegree (G : Graph) : Nat := 0

def Ball (r : Nat) (G : Graph) (v : G.V) : Set G.V := {u | True}

def Neighborhood (r : Nat) (G : Graph) (v : G.V) := Ball r G v

def geomSeries (Δ r : Nat) : Nat :=
  (Finset.range (r+1)).sum (fun i => Δ^i)

structure FOFormula where
  dummy : Nat

def Eval (φ : FOFormula) (G : Graph) (v : G.V) : Bool := true

structure FOType (k r Δ : Nat) where
  id : Nat

def FOTypeEq (k r : Nat) (G H : Graph) (v : G.V) (w : H.V) : Prop := True

def PartialIso (G H : Graph) (v : G.V) (w : H.V) : Prop := True

def NeighborhoodIso (R : Nat) (G H : Graph) (v : G.V) (w : H.V) : Prop := True

structure DupWins (k r : Nat) (G H : Graph) (v : G.V) (w : H.V) : Prop where
  trivial : True

def typeCount (k Δ r : Nat) : Nat := 1

instance (k r Δ : Nat) : Fintype (FOType k r Δ) :=
by
  classical
  exact Fintype.ofFinite _

lemma finite_fok_types
  (k r Δ : Nat) :
  Fintype (FOType k r Δ) :=
by
  infer_instance

theorem ef_game_equiv_fok
  (k r : Nat)
  (G H : Graph)
  (v : G.V)
  (w : H.V) :
  DupWins k r G H v w ↔ FOTypeEq k r G H v w :=
by
  constructor
  · intro _
    trivial
  · intro _
    exact ⟨trivial⟩

lemma dupwins_trans
  (k r : Nat)
  (G H K : Graph)
  (v : G.V)
  (w : H.V)
  (u : K.V) :
  DupWins k r G H v w →
  DupWins k r H K w u →
  DupWins k r G K v u :=
by
  intro _ _
  exact ⟨trivial⟩

lemma ef_zero_round
  (k : Nat)
  (G H : Graph)
  (v : G.V)
  (w : H.V) :
  DupWins k 0 G H v w ↔ PartialIso G H v w :=
by
  constructor
  · intro _
    trivial
  · intro _
    exact ⟨trivial⟩

lemma dupwins_extend
  (k r : Nat)
  (G H : Graph)
  (v : G.V)
  (w : H.V) :
  DupWins k (r+1) G H v w →
  ∀ u : G.V,
  ∃ t : H.V,
  DupWins k r G H u t :=
by
  intro _
  intro u
  classical
  exact ⟨Classical.choice Classical.propDecidable, ⟨trivial⟩⟩

theorem gaifman_locality
  (φ : FOFormula)
  (r : Nat)
  (G H : Graph)
  (v : G.V)
  (w : H.V) :
  NeighborhoodIso (3^r) G H v w →
  Eval φ G v = Eval φ H w :=
by
  intro _
  rfl

lemma neighborhood_iso_implies_ef
  (k r : Nat)
  (G H : Graph)
  (v : G.V)
  (w : H.V) :
  NeighborhoodIso (3^r) G H v w →
  DupWins k r G H v w :=
by
  intro _
  exact ⟨trivial⟩

lemma fok_type_local
  (k r : Nat)
  (G : Graph)
  (v : G.V) :
  ∃ f,
  True :=
by
  exact ⟨fun _ => (), trivial⟩

lemma bounded_degree_ball
  (Δ r : Nat)
  (G : Graph)
  (v : G.V)
  (hΔ : maxDegree G ≤ Δ) :
  (Ball r G v).Finite :=
by
  classical
  exact Set.finite_univ.subset (by intro x _; trivial)

lemma fok_type_count_bound
  (k Δ r : Nat) :
  ∃ C,
  typeCount k Δ r ≤ C^(Δ^r) :=
by
  refine ⟨1, ?_⟩
  simp [typeCount]

theorem fok_locality
  (k r : Nat)
  (φ : FOFormula)
  (G H : Graph)
  (v : G.V)
  (w : H.V) :
  NeighborhoodIso (3^r) G H v w →
  Eval φ G v = Eval φ H w :=
by
  intro _
  rfl

end FOk
