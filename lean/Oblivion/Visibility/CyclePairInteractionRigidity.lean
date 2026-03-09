import Mathlib.Data.Finset.Basic

namespace Oblivion

class FiniteGraph (V : Type) where
  adj : V -> V -> Prop

def CyclePairInteractionRank {V : Type} [Finite V] [FiniteGraph V] : Nat := 0

def FOkLocalTypeCount {V : Type} [Finite V] [FiniteGraph V] (k R : Nat) : Nat := 0

def LinearIn (f : Nat -> Nat) : Prop :=
  ∃ c N : Nat, c > 0 ∧ ∀ n ≥ N, f n ≥ c * n

theorem cpi_rigidity_conjectural
  (GraphSeq : Nat -> Type)
  [∀ n, Finite (GraphSeq n)]
  [∀ n, FiniteGraph (GraphSeq n)] :
  ∃ k0 R0 : Nat,
    k0 ≥ 5 ∧
    (LinearIn (fun n => CyclePairInteractionRank (V := GraphSeq n)) ->
     LinearIn (fun n => FOkLocalTypeCount (V := GraphSeq n) k0 R0)) := by
  sorry

end Oblivion
