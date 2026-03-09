import Mathlib.Data.Finset.Basic

namespace Oblivion

class FiniteGraph (V : Type) where
  adj : V -> V -> Prop

def CycleOverlapRank {V : Type} [Finite V] [FiniteGraph V] : Nat := 0

def PairOverlapProfile {V : Type} [Finite V] [FiniteGraph V] : Nat := 0

def RefinedCycleOverlapRank {V : Type} [Finite V] [FiniteGraph V] : Nat × Nat :=
  (CycleOverlapRank (V := V), PairOverlapProfile (V := V))

def FO4PairSignatureCount {V : Type} [Finite V] [FiniteGraph V] (R : Nat) : Nat := 0

def LinearIn (f : Nat -> Nat) : Prop :=
  ∃ c N : Nat, c > 0 ∧ ∀ n ≥ N, f n ≥ c * n

theorem pair_overlap_visibility_conjectural
  (GraphSeq : Nat -> Type)
  [∀ n, Finite (GraphSeq n)]
  [∀ n, FiniteGraph (GraphSeq n)] :
  ∃ R0 : Nat,
    (LinearIn (fun n => (RefinedCycleOverlapRank (V := GraphSeq n)).1) ->
     LinearIn (fun n => FO4PairSignatureCount (V := GraphSeq n) R0)) := by
  sorry

end Oblivion
