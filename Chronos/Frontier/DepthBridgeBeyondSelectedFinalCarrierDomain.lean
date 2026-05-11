import Chronos.Frontier.H4_1_FGL_FinalCarrierExtractionClosed

namespace Chronos
namespace Frontier

def DepthBridgeBeyondSelectedFinalCarrierDomain : Prop :=
  ∀ P : Predicate,
    RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily P →
    ∃ D : H4_1_FGL_SelectedTheoremDomain,
      depth_bridge_admissibility D

theorem depth_bridge_beyond_selected_final_carrier_domain_generated :
    DepthBridgeBeyondSelectedFinalCarrierDomain := by
  intro P hP
  exact H4_1_FGL_final_carrier_depth_bridge_surface P hP

end Frontier
end Chronos
