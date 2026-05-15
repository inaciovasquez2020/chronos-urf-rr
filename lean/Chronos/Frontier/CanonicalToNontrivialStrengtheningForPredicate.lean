import Chronos.Frontier.NontrivialFiberEntropyGapPredicate

namespace Chronos
namespace Frontier

/--
The strengthening interface closes for the repository-defined
NontrivialFiberEntropyGapPredicate.

This is theorem-producing only for the predicate surface already defined as
the canonical zero-entropy gap. It is not a construction of a genuinely
nontrivial universal fiber-entropy gap.
-/
theorem canonical_to_nontrivial_strengthening_for_predicate
    (α : Type)
    (entropyDefect : α → Nat) :
    CanonicalToNontrivialFiberEntropyGapStrengthening
      α entropyDefect
      (NontrivialFiberEntropyGapPredicate α entropyDefect) := by
  intro X hcanonical
  exact canonical_zero_entropy_implies_nontrivial_fiber_entropy_gap_predicate
    α entropyDefect X hcanonical

theorem semantic_rank_rate_soundness_implies_defined_nontrivial_fiber_gap
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (soundness : SemanticRankRateToFiberEntropySoundness α rankDefect entropyDefect)
    (X : α)
    (hrank : rankDefect X = 0) :
    NontrivialFiberEntropyGapPredicate α entropyDefect X :=
  semantic_rank_rate_soundness_implies_nontrivial_fiber_gap
    α rankDefect entropyDefect
    (NontrivialFiberEntropyGapPredicate α entropyDefect)
    soundness
    (canonical_to_nontrivial_strengthening_for_predicate α entropyDefect)
    X
    hrank

theorem semantic_rank_defect_control_implies_defined_nontrivial_fiber_gap
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (control : SemanticRankDefectControlsEntropyDefectOn α rankDefect entropyDefect)
    (X : α)
    (hrank : rankDefect X = 0) :
    NontrivialFiberEntropyGapPredicate α entropyDefect X :=
  semantic_rank_defect_control_implies_nontrivial_fiber_gap
    α rankDefect entropyDefect
    (NontrivialFiberEntropyGapPredicate α entropyDefect)
    control
    (canonical_to_nontrivial_strengthening_for_predicate α entropyDefect)
    X
    hrank

end Frontier
end Chronos
