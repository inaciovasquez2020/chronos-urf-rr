import Lean.CLR.EFGame

universe u

open Classical

lemma EFWin.symm
  (q k : Nat) :
  ∀ {A B : RootedBallSig},
    EFWin q k A B → EFWin q k B A := by
  intro A B h
  induction h with
  | zero k A B h0 =>
      exact EFWin.zero k B A (by simpa using h0)
  | succ_left q k A B h ih =>
      exact EFWin.succ_right q k B A (by
        intro b
        have := h
        classical
        exact ⟨Classical.choice ⟨A.root⟩, ih (Classical.choice ⟨A.root⟩)⟩)
  | succ_right q k A B h ih =>
      exact EFWin.succ_left q k B A (by
        intro a
        have := h
        classical
        exact ⟨Classical.choice ⟨B.root⟩, ih (Classical.choice ⟨B.root⟩)⟩)

lemma EFWin.trans
  (q k : Nat) :
  ∀ {A B C : RootedBallSig},
    EFWin q k A B →
    EFWin q k B C →
    EFWin q k A C := by
  intro A B C hAB hBC
  induction hAB generalizing C with
  | zero k A B h0 =>
      simpa using hBC
  | succ_left q k A B hAB ih =>
      exact EFWin.succ_left q k A C (by
        intro a
        obtain ⟨b, hab⟩ := hAB a
        obtain ⟨c, hbc⟩ := Classical.choice ⟨C.root, hBC⟩
        exact ⟨c, ih hab hBC⟩)
  | succ_right q k A B hAB ih =>
      exact EFWin.succ_right q k A C (by
        intro c
        obtain ⟨b, hbc⟩ := Classical.choice ⟨B.root, hBC⟩
        obtain ⟨a, hab⟩ := hAB b
        exact ⟨a, ih hab hBC⟩)
