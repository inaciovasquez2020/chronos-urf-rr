import Chronos.Frontier.CanonicalZeroEntropyFiberGapMinimality

namespace Chronos
namespace Frontier

/--
Strengthening interface from the canonical zero-entropy fiber-gap predicate
to a nontrivial fiber-gap predicate.

This does not construct the nontrivial predicate.
It isolates the exact remaining strengthening obligation.
-/
def CanonicalToNontrivialFiberEntropyGapStrengthening
    (α : Type)
    (entropyDefect : α → Nat)
    (nontrivialFiberEntropyGap : α → Prop) : Prop :=
  ∀ X : α,
    CanonicalZeroEntropyFiberGap α entropyDefect X →
    nontrivialFiberEntropyGap X

theorem canonical_strengthening_implies_nontrivial_fiber_gap
    (α : Type)
    (entropyDefect : α → Nat)
    (nontrivialFiberEntropyGap : α → Prop)
    (strengthening :
      CanonicalToNontrivialFiberEntropyGapStrengthening
        α entropyDefect nontrivialFiberEntropyGap)
    (X : α)
    (hcanonical : CanonicalZeroEntropyFiberGap α entropyDefect X) :
    nontrivialFiberEntropyGap X :=
  strengthening X hcanonical

theorem semantic_rank_rate_soundness_implies_nontrivial_fiber_gap
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (nontrivialFiberEntropyGap : α → Prop)
    (soundness : SemanticRankRateToFiberEntropySoundness α rankDefect entropyDefect)
    (strengthening :
      CanonicalToNontrivialFiberEntropyGapStrengthening
        α entropyDefect nontrivialFiberEntropyGap)
    (X : α)
    (hrank : rankDefect X = 0) :
    nontrivialFiberEntropyGap X :=
  canonical_strengthening_implies_nontrivial_fiber_gap
    α entropyDefect nontrivialFiberEntropyGap
    strengthening X
    (semantic_rank_rate_soundness_implies_canonical_zero_entropy_fiber_gap
      α rankDefect entropyDefect soundness X hrank)

theorem semantic_rank_defect_control_implies_nontrivial_fiber_gap
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (nontrivialFiberEntropyGap : α → Prop)
    (control : SemanticRankDefectControlsEntropyDefectOn α rankDefect entropyDefect)
    (strengthening :
      CanonicalToNontrivialFiberEntropyGapStrengthening
        α entropyDefect nontrivialFiberEntropyGap)
    (X : α)
    (hrank : rankDefect X = 0) :
    nontrivialFiberEntropyGap X :=
  canonical_strengthening_implies_nontrivial_fiber_gap
    α entropyDefect nontrivialFiberEntropyGap
    strengthening X
    (semantic_rank_defect_control_implies_canonical_zero_entropy_fiber_gap
      α rankDefect entropyDefect control X hrank)

end Frontier
end Chronos
