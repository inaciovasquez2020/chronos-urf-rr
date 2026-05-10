import Chronos.Frontier.FinalCarrierObservationExtraction

namespace Chronos
namespace Frontier

/--
Final-carrier extraction closure surface.

This promotes the already-merged final carrier observation extraction bridge to
an exported H4.1/FGL closure surface over unrestricted admissible predicates,
with the boundary limited to selected-domain gap, fiber, and depth admissibility.
-/
theorem H4_1_FGL_final_carrier_extraction_closed
    (P : Predicate)
    (hP : RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily P) :
    ∃ D : H4_1_FGL_SelectedTheoremDomain,
      gap_soundness D ∧
      fiber_entropy_gap D ∧
      depth_bridge_admissibility D :=
  final_carrier_observation_extraction_closed P hP

/--
Gap-soundness projection of the final-carrier extraction closure surface.
-/
theorem H4_1_FGL_final_carrier_gap_soundness_surface
    (P : Predicate)
    (hP : RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily P) :
    ∃ D : H4_1_FGL_SelectedTheoremDomain,
      gap_soundness D := by
  rcases H4_1_FGL_final_carrier_extraction_closed P hP with
    ⟨D, hgap, _hfiber, _hdepth⟩
  exact ⟨D, hgap⟩

/--
Fiber-entropy projection of the final-carrier extraction closure surface.
-/
theorem H4_1_FGL_final_carrier_fiber_entropy_surface
    (P : Predicate)
    (hP : RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily P) :
    ∃ D : H4_1_FGL_SelectedTheoremDomain,
      fiber_entropy_gap D := by
  rcases H4_1_FGL_final_carrier_extraction_closed P hP with
    ⟨D, _hgap, hfiber, _hdepth⟩
  exact ⟨D, hfiber⟩

/--
Depth-bridge admissibility projection of the final-carrier extraction closure surface.
-/
theorem H4_1_FGL_final_carrier_depth_bridge_surface
    (P : Predicate)
    (hP : RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily P) :
    ∃ D : H4_1_FGL_SelectedTheoremDomain,
      depth_bridge_admissibility D := by
  rcases H4_1_FGL_final_carrier_extraction_closed P hP with
    ⟨D, _hgap, _hfiber, hdepth⟩
  exact ⟨D, hdepth⟩

end Frontier
end Chronos
