import Lean.CLR.EFGame
import Lean.CLR.EFWinLemmas

universe u

def foEquiv (Δ R k q : Nat) (A B : RootedBallSig) : Prop :=
  fo_equiv_k_q_on_balls Δ R k q A B

lemma foEquiv_refl (Δ R k q : Nat) (A : RootedBallSig) :
  foEquiv Δ R k q A A :=
  fo_equiv_refl Δ R k q A

lemma foEquiv_symm (Δ R k q : Nat) :
  ∀ {A B : RootedBallSig},
    foEquiv Δ R k q A B →
    foEquiv Δ R k q B A :=
by
  intro A B h
  exact EFWin.symm q k h

lemma foEquiv_trans (Δ R k q : Nat) :
  ∀ {A B C : RootedBallSig},
    foEquiv Δ R k q A B →
    foEquiv Δ R k q B C →
    foEquiv Δ R k q A C :=
by
  intro A B C hAB hBC
  exact EFWin.trans q k hAB hBC

instance foEquivSetoid (Δ R k q : Nat) : Setoid RootedBallSig where
  r := foEquiv Δ R k q
  iseqv :=
  ⟨
    foEquiv_refl Δ R k q,
    foEquiv_symm Δ R k q,
    foEquiv_trans Δ R k q
  ⟩
