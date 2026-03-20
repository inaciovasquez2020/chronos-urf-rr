import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fin.Basic

universe u

structure RootedBallSig where
  V : Type u
  [fV : Fintype V]
  [dV : DecidableEq V]
  adj : V → V → Prop
  [decAdj : DecidableRel adj]
  root : V
  deg_bound : Nat

attribute [instance] RootedBallSig.fV RootedBallSig.dV RootedBallSig.decAdj

inductive EFGameState (k : Nat) (A B : RootedBallSig) where
  | mk : (Fin k → Option A.V) → (Fin k → Option B.V) → EFGameState k A B

namespace EFGameState

def partialIso {k : Nat} {A B : RootedBallSig} : EFGameState k A B → Prop
  | .mk a b =>
      (∀ i, (a i).isSome ↔ (b i).isSome) ∧
      (∀ i j,
        match a i, a j, b i, b j with
        | some x, some y, some x', some y' =>
            (x = y ↔ x' = y') ∧ (A.adj x y ↔ B.adj x' y')
        | none, none, none, none => True
        | _, _, _, _ => False)

end EFGameState

inductive EFWin : Nat → Nat → RootedBallSig → RootedBallSig → Prop
  | zero (k : Nat) (A B : RootedBallSig) :
      EFGameState.partialIso (.mk (fun _ => none) (fun _ => none)) →
      EFWin 0 k A B
  | succ_left (q k : Nat) (A B : RootedBallSig) :
      (∀ a : A.V, ∃ b : B.V, EFWin q k A B) →
      EFWin (q+1) k A B
  | succ_right (q k : Nat) (A B : RootedBallSig) :
      (∀ b : B.V, ∃ a : A.V, EFWin q k A B) →
      EFWin (q+1) k A B

def fo_equiv_k_q_on_balls (Δ R k q : Nat) (A B : RootedBallSig) : Prop :=
  EFWin q k A B

theorem fo_equiv_refl (Δ R k q : Nat) (A : RootedBallSig) :
    fo_equiv_k_q_on_balls Δ R k q A A := by
  induction q with
  | zero =>
      exact EFWin.zero k A A (by
        refine ⟨?_, ?_⟩
        · intro i; simp
        · intro i j; simp)
  | succ q ih =>
      exact EFWin.succ_left q k A A (by
        intro a; exact ⟨a, ih⟩)
