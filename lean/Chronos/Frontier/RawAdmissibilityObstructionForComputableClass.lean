import Chronos.Frontier.StructuredAdmissibilityDominanceForComputableClass

namespace Chronos
namespace Frontier

/--
Counterexample showing that opaque raw admissibility alone is too weak.

The object is admissible, finite, and computable, but has
`SemanticRankRate = 1` and `FiberEntropyGap = 0`.
-/
def rawAdmissibilityCounterexample : ComputableFiniteAdmissibleClass where
  objectCount := 1
  semanticRankRate := 1
  fiberEntropyGap := 0
  admissible := True
  finite_support := by decide
  semantic_rank_rate_computable := ⟨1, rfl⟩
  fiber_entropy_gap_computable := ⟨0, rfl⟩

theorem raw_admissibility_counterexample_admissible :
    rawAdmissibilityCounterexample.admissible := by
  trivial

theorem raw_admissibility_counterexample_no_bridge :
    ¬ SemanticRankRate rawAdmissibilityCounterexample ≤
      FiberEntropyGap rawAdmissibilityCounterexample := by
  decide

theorem not_raw_to_structured_admissibility_dominance :
    ¬ RawToStructuredAdmissibilityDominance := by
  intro lift
  exact raw_admissibility_counterexample_no_bridge
    (lift rawAdmissibilityCounterexample
      raw_admissibility_counterexample_admissible).rank_entropy_dominance

theorem not_finite_support_bridge_law_for_computable_class :
    ¬ FiniteSupportBridgeLawForComputableClass := by
  intro law
  exact raw_admissibility_counterexample_no_bridge
    (law rawAdmissibilityCounterexample
      raw_admissibility_counterexample_admissible)

theorem not_finite_support_bridge_certificate_supply :
    ¬ FiniteSupportBridgeCertificateSupply := by
  intro supply
  exact raw_admissibility_counterexample_no_bridge
    (supply rawAdmissibilityCounterexample
      raw_admissibility_counterexample_admissible).semantic_rank_le_entropy_gap

end Frontier
end Chronos
