import Chronos.Frontier.SemanticRankRateToFiberEntropySoundnessBridge

namespace Chronos
namespace Frontier

/--
Universal fiber-entropy-gap compatibility at the weakest semantic level.

This does not construct a universal fiber entropy gap.
It only records the exact bridge needed after semantic rank-rate soundness:
zero entropy defect implies the chosen gap predicate.
-/
def UniversalFiberEntropyGapCompatibility
    (α : Type)
    (entropyDefect : α → Nat)
    (fiberEntropyGap : α → Prop) : Prop :=
  ∀ X : α, entropyDefect X = 0 → fiberEntropyGap X

/--
Weakest compatibility bridge:

Semantic rank-rate soundness plus zero-entropy-gap compatibility implies
rank-zero universal fiber entropy gap compatibility.
-/
theorem semantic_rank_rate_soundness_implies_universal_fiber_entropy_gap_compatibility
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (fiberEntropyGap : α → Prop)
    (soundness : SemanticRankRateToFiberEntropySoundness α rankDefect entropyDefect)
    (compatibility : UniversalFiberEntropyGapCompatibility α entropyDefect fiberEntropyGap)
    (X : α)
    (hrank : rankDefect X = 0) :
    fiberEntropyGap X :=
  compatibility X (soundness X hrank)

/--
Derived compatibility from the stronger quantitative comparison surface.
-/
theorem semantic_rank_defect_control_implies_universal_fiber_entropy_gap_compatibility
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (fiberEntropyGap : α → Prop)
    (control : SemanticRankDefectControlsEntropyDefectOn α rankDefect entropyDefect)
    (compatibility : UniversalFiberEntropyGapCompatibility α entropyDefect fiberEntropyGap)
    (X : α)
    (hrank : rankDefect X = 0) :
    fiberEntropyGap X :=
  semantic_rank_rate_soundness_implies_universal_fiber_entropy_gap_compatibility
    α rankDefect entropyDefect fiberEntropyGap
    (semantic_rank_defect_control_implies_soundness α rankDefect entropyDefect control)
    compatibility X hrank

end Frontier
end Chronos
