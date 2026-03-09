import Mathlib.Data.Finset.Basic

namespace Oblivion

class FiniteGraph (V : Type) where
  adj : V -> V -> Prop

def CycleEdgeRank {V : Type} [Finite V] [FiniteGraph V] : Nat := 0

def CycleIntersectionRank {V : Type} [Finite V] [FiniteGraph V] : Nat := 0

def CyclePairInteractionRank {V : Type} [Finite V] [FiniteGraph V] : Nat := 0

def CyclePairInteractionInvariant {V : Type} [Finite V] [FiniteGraph V] : Nat × Nat × Nat :=
  (CycleEdgeRank (V := V), CycleIntersectionRank (V := V), CyclePairInteractionRank (V := V))

def FOkLocalTypeCount {V : Type} [Finite V] [FiniteGraph V] (k R : Nat) : Nat := 0

def LinearIn (f : Nat -> Nat) : Prop :=
  ∃ c N : Nat, c > 0 ∧ ∀ n ≥ N, f n ≥ c * n

theorem cycle_pair_interaction_rigidity_conjectural
  (GraphSeq : Nat -> Type)
  [∀ n, Finite (GraphSeq n)]
  [∀ n, FiniteGraph (GraphSeq n)] :
  ∃ k0 R0 : Nat,
    k0 ≥ 5 ∧
    (LinearIn (fun n => (CyclePairInteractionInvariant (V := GraphSeq n)).1) ->
     LinearIn (fun n => FOkLocalTypeCount (V := GraphSeq n) k0 R0)) := by
  sorry

end Oblivion
