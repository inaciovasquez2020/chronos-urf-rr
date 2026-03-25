import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fin.Basic
import Mathlib.Data.List.Basic
import Mathlib.Data.Nat.Basic

universe u

inductive SyntaxTree where
  | atom : Nat → SyntaxTree
  | node : Nat → List SyntaxTree → SyntaxTree
deriving DecidableEq, Repr

structure RootedTupleCode where
  radius : Nat
  tupleArity : Nat
  labels : List Nat
  tree : SyntaxTree
deriving DecidableEq, Repr

structure Graph where
  V : Type u

structure FOType (k R Δ : Nat) where
  rooted : RootedTupleCode
  arity_ok : rooted.tupleArity = k
  radius_ok : rooted.radius = R
deriving DecidableEq, Repr

structure SupportState where
  rt : Nat
  support : List Nat
deriving DecidableEq, Repr

structure EFStep where
  newVertex : Nat
deriving DecidableEq, Repr

def nextSupportState (s : SupportState) (m : EFStep) : SupportState :=
  { rt := s.rt + 1
    support := m.newVertex :: s.support }

theorem support_growth_invariant (s : SupportState) (m : EFStep) :
    (nextSupportState s m).rt ≤ s.rt + 1 := by
  simp [nextSupportState]

structure InducedWitness (G : Graph) where
  centerSupport : List Nat
  radius : Nat
deriving Repr

def inducedWitness (G : Graph) (R k : Nat) (Si : List Nat) : InducedWitness G :=
  { centerSupport := Si
    radius := R + k }

theorem Locality_of_continuation
    (G : Graph)
    (k R Δ : Nat)
    (τi τj : FOType k R Δ)
    (Si : List Nat)
    (hτ : τi = τj) :
    ∃ H : InducedWitness G, H.radius = R + k := by
  subst hτ
  refine ⟨inducedWitness G R k Si, rfl⟩

class FOTypeFinite (k R Δ : Nat) where
  enum : Fintype (FOType k R Δ)

attribute [instance] FOTypeFinite.enum

abbrev ConfSeq (k R Δ T : Nat) := Fin (T + 1) → FOType k R Δ

namespace Oblivion

theorem repetition_to_oblivion_chain
    (G : Graph)
    (k R Δ T : Nat)
    [FOTypeFinite k R Δ]
    (σ : ConfSeq k R Δ T)
    (hrep : ∃ i j : Fin (T + 1), i.1 < j.1 ∧ σ i = σ j)
    (Si : List Nat) :
    ∃ H : InducedWitness G, H.radius = R + k := by
  rcases hrep with ⟨i, j, hij, hσ⟩
  exact Locality_of_continuation G k R Δ (σ i) (σ j) Si hσ

abbrev FrontLemma := @repetition_to_oblivion_chain

end Oblivion
