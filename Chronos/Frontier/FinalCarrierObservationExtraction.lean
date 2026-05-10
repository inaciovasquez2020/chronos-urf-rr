import Chronos.Frontier.H4_1_FGL_FinalSoundnessFrontier
import Chronos.Frontier.H4_1_FGL_RestrictedDomainReduction
import Chronos.Frontier.PositiveArityRepositoryNativeCoverage
import Chronos.Frontier.SelectedCarrierObservationDimensionExtraction
import Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap
import Chronos.Frontier.ZeroArityRepresentationInterface

namespace Chronos
namespace Frontier

theorem zero_arity_selected_domain_absorption
    (P : Predicate)
    (hP : RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily P)
    (h0 : P.arity = 0) :
    ∃ D : H4_1_FGL_SelectedTheoremDomain,
      D = SelectedDomainInjector.fromZeroArity
            P
            (ZeroArityRepresentationInterface.represent P ⟨h0, hP⟩) ∧
      gap_soundness D ∧
      fiber_entropy_gap D ∧
      depth_bridge_admissibility D := by
  let rep := ZeroArityRepresentationInterface.represent P ⟨h0, hP⟩
  let D := SelectedDomainInjector.fromZeroArity P rep
  refine ⟨D, rfl, ?_, ?_, ?_⟩
  · exact ZeroArityRepresentationInterface.soundness_trivial P h0 hP
  · exact ZeroArityRepresentationInterface.entropy_gap_zero P h0 hP
  · exact ZeroArityRepresentationInterface.depth_bridge_admissible P h0 hP

theorem positive_arity_selected_domain_absorption
    (P : Predicate)
    (hP : RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily P)
    (hpos : 0 < P.arity) :
    ∃ D : H4_1_FGL_SelectedTheoremDomain,
      D = SelectedDomainInjector.fromPositiveArity P hpos hP ∧
      gap_soundness D ∧
      fiber_entropy_gap D ∧
      depth_bridge_admissibility D := by
  let D := SelectedDomainInjector.fromPositiveArity P hpos hP
  refine ⟨D, rfl, ?_, ?_, ?_⟩
  · exact SelectedCarrierObservationDimensionExtraction.soundness_inherited P hpos hP
  · exact SelectedCarrierDepthBridgeFiberGap.selected_carrier_fiber_entropy_gap P hpos hP
  · exact PositiveArityRepositoryNativeCoverage.positive_arity_coverage_implies_reg_snf P hpos hP

theorem final_carrier_observation_extraction_closed
    (P : Predicate)
    (hP : RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily P) :
    ∃ D : H4_1_FGL_SelectedTheoremDomain,
      gap_soundness D ∧
      fiber_entropy_gap D ∧
      depth_bridge_admissibility D := by
  by_cases h0 : P.arity = 0
  · rcases zero_arity_selected_domain_absorption P hP h0 with
      ⟨D, _hD, hgap, hfiber, hdepth⟩
    exact ⟨D, hgap, hfiber, hdepth⟩
  · have hpos : 0 < P.arity := Nat.pos_of_ne_zero h0
    rcases positive_arity_selected_domain_absorption P hP hpos with
      ⟨D, _hD, hgap, hfiber, hdepth⟩
    exact ⟨D, hgap, hfiber, hdepth⟩

end Frontier
end Chronos
