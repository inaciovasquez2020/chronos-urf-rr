import Chronos.Frontier.NontrivialFiberEntropyGapStrengthening

namespace Chronos
namespace Frontier

/--
Canonical nontrivial-fiber-entropy-gap predicate surface.

The predicate is intentionally defined as the weakest predicate containing
the canonical zero-entropy gap.  It is a predicate surface, not a construction
of a genuinely nontrivial universal fiber-entropy gap.
-/
def NontrivialFiberEntropyGapPredicate
    (α : Type)
    (entropyDefect : α → Nat) : α → Prop :=
  fun X => CanonicalZeroEntropyFiberGap α entropyDefect X

/--
Relation to a chosen UniversalFiberEntropyGap predicate.

This says the canonical predicate surface is contained in the chosen universal
fiber-entropy-gap predicate.
-/
def NontrivialFiberEntropyGapRefinesUniversal
    (α : Type)
    (entropyDefect : α → Nat)
    (universalFiberEntropyGap : α → Prop) : Prop :=
  ∀ X : α,
    NontrivialFiberEntropyGapPredicate α entropyDefect X →
    universalFiberEntropyGap X

theorem canonical_zero_entropy_implies_nontrivial_fiber_entropy_gap_predicate
    (α : Type)
    (entropyDefect : α → Nat)
    (X : α)
    (hcanonical : CanonicalZeroEntropyFiberGap α entropyDefect X) :
    NontrivialFiberEntropyGapPredicate α entropyDefect X :=
  hcanonical

theorem universal_compatibility_implies_nontrivial_refines_universal
    (α : Type)
    (entropyDefect : α → Nat)
    (universalFiberEntropyGap : α → Prop)
    (compatibility :
      UniversalFiberEntropyGapCompatibility
        α entropyDefect universalFiberEntropyGap) :
    NontrivialFiberEntropyGapRefinesUniversal
      α entropyDefect universalFiberEntropyGap := by
  intro X hnontrivial
  exact compatibility X hnontrivial

theorem semantic_rank_rate_soundness_implies_nontrivial_fiber_entropy_gap_predicate
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (soundness : SemanticRankRateToFiberEntropySoundness α rankDefect entropyDefect)
    (X : α)
    (hrank : rankDefect X = 0) :
    NontrivialFiberEntropyGapPredicate α entropyDefect X :=
  canonical_zero_entropy_implies_nontrivial_fiber_entropy_gap_predicate
    α entropyDefect X
    (semantic_rank_rate_soundness_implies_canonical_zero_entropy_fiber_gap
      α rankDefect entropyDefect soundness X hrank)

theorem semantic_rank_rate_soundness_implies_universal_from_nontrivial_relation
    (α : Type)
    (rankDefect entropyDefect : α → Nat)
    (universalFiberEntropyGap : α → Prop)
    (soundness : SemanticRankRateToFiberEntropySoundness α rankDefect entropyDefect)
    (relation :
      NontrivialFiberEntropyGapRefinesUniversal
        α entropyDefect universalFiberEntropyGap)
    (X : α)
    (hrank : rankDefect X = 0) :
    universalFiberEntropyGap X :=
  relation X
    (semantic_rank_rate_soundness_implies_nontrivial_fiber_entropy_gap_predicate
      α rankDefect entropyDefect soundness X hrank)

end Frontier
end Chronos
