namespace Chronos
namespace Frontier

/--
Weakest sufficient replacement for the stronger pointwise control lemma.

Instead of proving a quantitative inequality
  entropyDefect X ≤ rankDefect X,
the downstream bridge only requires the zero-defect implication:
  rankDefect X = 0 → entropyDefect X = 0.
-/
def SemanticRankZeroDefectKillsEntropyDefectOn
    (α : Type)
    (rankDefect entropyDefect : α → Nat) : Prop :=
  ∀ X : α, rankDefect X = 0 → entropyDefect X = 0

/--
Stronger original target, retained as a comparison surface only.
-/
def SemanticRankDefectControlsEntropyDefectOn
    (α : Type)
    (rankDefect entropyDefect : α → Nat) : Prop :=
  ∀ X : α, entropyDefect X ≤ rankDefect X

theorem semantic_rank_defect_control_implies_zero_defect_transfer
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (h : SemanticRankDefectControlsEntropyDefectOn α rankDefect entropyDefect) :
    SemanticRankZeroDefectKillsEntropyDefectOn α rankDefect entropyDefect := by
  intro X hzero
  exact Nat.eq_zero_of_le_zero (by simpa [hzero] using h X)

/--
Conditional replacement theorem.

The weaker sufficient lemma is enough to transfer zero semantic rank defect
to zero entropy defect.
-/
theorem semantic_rank_zero_defect_transfer
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (h : SemanticRankZeroDefectKillsEntropyDefectOn α rankDefect entropyDefect)
    (X : α)
    (hr : rankDefect X = 0) :
    entropyDefect X = 0 :=
  h X hr

end Frontier
end Chronos
