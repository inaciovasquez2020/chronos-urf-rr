import Chronos.Frontier.CanonicalZeroEntropyFiberGapCompatibility

namespace Chronos
namespace Frontier

/--
Minimality of the canonical zero-entropy fiber-gap predicate.

Any fiber-gap predicate compatible with zero entropy defect must contain
the canonical zero-entropy predicate.
-/
def CanonicalZeroEntropyFiberGapContainedIn
    (α : Type)
    (entropyDefect : α → Nat)
    (fiberEntropyGap : α → Prop) : Prop :=
  ∀ X : α,
    CanonicalZeroEntropyFiberGap α entropyDefect X →
    fiberEntropyGap X

theorem canonical_zero_entropy_fiber_gap_minimality
    (α : Type)
    (entropyDefect : α → Nat)
    (fiberEntropyGap : α → Prop)
    (compatibility :
      UniversalFiberEntropyGapCompatibility α entropyDefect fiberEntropyGap) :
    CanonicalZeroEntropyFiberGapContainedIn α entropyDefect fiberEntropyGap := by
  intro X hzero
  exact compatibility X hzero

theorem canonical_zero_entropy_fiber_gap_self_minimality
    (α : Type)
    (entropyDefect : α → Nat) :
    CanonicalZeroEntropyFiberGapContainedIn
      α entropyDefect
      (CanonicalZeroEntropyFiberGap α entropyDefect) := by
  intro X hzero
  exact hzero

theorem semantic_rank_rate_soundness_implies_any_compatible_fiber_gap
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (fiberEntropyGap : α → Prop)
    (soundness : SemanticRankRateToFiberEntropySoundness α rankDefect entropyDefect)
    (compatibility :
      UniversalFiberEntropyGapCompatibility α entropyDefect fiberEntropyGap)
    (X : α)
    (hrank : rankDefect X = 0) :
    fiberEntropyGap X :=
  canonical_zero_entropy_fiber_gap_minimality
    α entropyDefect fiberEntropyGap compatibility
    X
    (semantic_rank_rate_soundness_implies_canonical_zero_entropy_fiber_gap
      α rankDefect entropyDefect soundness X hrank)

theorem semantic_rank_defect_control_implies_any_compatible_fiber_gap
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (fiberEntropyGap : α → Prop)
    (control : SemanticRankDefectControlsEntropyDefectOn α rankDefect entropyDefect)
    (compatibility :
      UniversalFiberEntropyGapCompatibility α entropyDefect fiberEntropyGap)
    (X : α)
    (hrank : rankDefect X = 0) :
    fiberEntropyGap X :=
  canonical_zero_entropy_fiber_gap_minimality
    α entropyDefect fiberEntropyGap compatibility
    X
    (semantic_rank_defect_control_implies_canonical_zero_entropy_fiber_gap
      α rankDefect entropyDefect control X hrank)

end Frontier
end Chronos
