import Chronos.Frontier.SemanticRankDefectControlsEntropyDefectOn

namespace Chronos
namespace Frontier

/--
Semantic rank-rate to fiber-entropy soundness, at the weakest zero-defect level.

This is intentionally not the quantitative inequality
  entropyDefect X ≤ rankDefect X.

It only asserts that zero semantic rank defect forces zero entropy defect.
-/
def SemanticRankRateToFiberEntropySoundness
    (α : Type)
    (rankDefect entropyDefect : α → Nat) : Prop :=
  ∀ X : α, rankDefect X = 0 → entropyDefect X = 0

theorem semantic_rank_zero_defect_kills_entropy_defect_implies_soundness
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (h : SemanticRankZeroDefectKillsEntropyDefectOn α rankDefect entropyDefect) :
    SemanticRankRateToFiberEntropySoundness α rankDefect entropyDefect := by
  intro X hzero
  exact h X hzero

theorem semantic_rank_defect_control_implies_soundness
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (h : SemanticRankDefectControlsEntropyDefectOn α rankDefect entropyDefect) :
    SemanticRankRateToFiberEntropySoundness α rankDefect entropyDefect := by
  exact semantic_rank_zero_defect_kills_entropy_defect_implies_soundness
    α rankDefect entropyDefect
    (semantic_rank_defect_control_implies_zero_defect_transfer
      α rankDefect entropyDefect h)

end Frontier
end Chronos
