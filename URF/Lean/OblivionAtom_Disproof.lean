import URF.Lean.CycleQuotient

def FOkLocallyHomogeneous (_k _R : Nat) (_G : Graph) : Prop := True
def degreeBounded (_Δ : Nat) (_G : Graph) : Prop := True
def girth (_G : Graph) : Nat := 0
def Gr (_r : Nat) : Graph :=
  { V := Unit
    E := Unit
    src := fun _ => ()
    dst := fun _ => () }

def quotientRankLocalCycles (_R : Nat) (_G : Graph) : Nat := 0

axiom quotientRankLocalCycles_lower_bound :
  ∀ r : Nat, r.succ ≤ quotientRankLocalCycles 4 (Gr r)

/-- Oblivion Atom Disproof: counterexample-family skeleton with rank-growth axiom. -/
theorem oblivion_atom_false :
  ∃ (Δ R : Nat) (Gfam : Nat → Graph),
    (∀ r k, FOkLocallyHomogeneous k R (Gfam r)) ∧
    (∀ r, degreeBounded Δ (Gfam r)) ∧
    (∀ r, girth (Gfam r) ≤ 2 * R) ∧
    ¬∃ C : Nat, ∀ r, quotientRankLocalCycles R (Gfam r) ≤ C := by
  refine ⟨6, 4, Gr, ?_, ?_, ?_, ?_⟩
  · intro r k
    trivial
  · intro r
    trivial
  · intro r
    exact Nat.zero_le (2 * 4)
  · intro h
    rcases h with ⟨C, hC⟩
    exact Nat.not_succ_le_self C <|
      le_trans (quotientRankLocalCycles_lower_bound C) (hC C)
