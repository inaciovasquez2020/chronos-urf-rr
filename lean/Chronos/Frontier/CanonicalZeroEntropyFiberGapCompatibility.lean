import Chronos.Frontier.SemanticRankRateUniversalFiberEntropyGapCompatibility

namespace Chronos
namespace Frontier

/--
Canonical weakest fiber-gap predicate induced by zero entropy defect.

This is not a nontrivial construction of UniversalFiberEntropyGap.
It only records the minimal predicate for which compatibility is immediate.
-/
def CanonicalZeroEntropyFiberGap
    (α : Type)
    (entropyDefect : α → Nat) : α → Prop :=
  fun X => entropyDefect X = 0

theorem canonical_zero_entropy_fiber_gap_compatibility
    (α : Type)
    (entropyDefect : α → Nat) :
    UniversalFiberEntropyGapCompatibility
      α entropyDefect
      (CanonicalZeroEntropyFiberGap α entropyDefect) := by
  intro X hzero
  exact hzero

theorem semantic_rank_rate_soundness_implies_canonical_zero_entropy_fiber_gap
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (soundness : SemanticRankRateToFiberEntropySoundness α rankDefect entropyDefect)
    (X : α)
    (hrank : rankDefect X = 0) :
    CanonicalZeroEntropyFiberGap α entropyDefect X :=
  semantic_rank_rate_soundness_implies_universal_fiber_entropy_gap_compatibility
    α rankDefect entropyDefect
    (CanonicalZeroEntropyFiberGap α entropyDefect)
    soundness
    (canonical_zero_entropy_fiber_gap_compatibility α entropyDefect)
    X
    hrank

theorem semantic_rank_defect_control_implies_canonical_zero_entropy_fiber_gap
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (control : SemanticRankDefectControlsEntropyDefectOn α rankDefect entropyDefect)
    (X : α)
    (hrank : rankDefect X = 0) :
    CanonicalZeroEntropyFiberGap α entropyDefect X :=
  semantic_rank_defect_control_implies_universal_fiber_entropy_gap_compatibility
    α rankDefect entropyDefect
    (CanonicalZeroEntropyFiberGap α entropyDefect)
    control
    (canonical_zero_entropy_fiber_gap_compatibility α entropyDefect)
    X
    hrank

end Frontier
end Chronos
