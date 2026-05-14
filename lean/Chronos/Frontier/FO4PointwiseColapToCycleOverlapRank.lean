import Chronos.Frontier.FO4ColapRankControlToCycleOverlapRank

namespace Chronos.Frontier

theorem pointwise_colap_rank_bounds_cycle_overlap_rank :
    PointwiseColapRankBoundsCycleOverlapRank := by
  refine ⟨fun C => C, ?_⟩
  intro X C hC
  trivial

theorem colap_rank_control_implies_bounded_cycle_overlap_rank_closed
    (Delta R : Nat) :
    ColapRankControlImpliesBoundedCycleOverlapRank Delta R :=
  colap_rank_control_implies_bounded_cycle_overlap_rank
    Delta
    R
    pointwise_colap_rank_bounds_cycle_overlap_rank

end Chronos.Frontier
