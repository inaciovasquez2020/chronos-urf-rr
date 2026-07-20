import Chronos.Frontier.R2Geometry.R2MetricFillingGeometry

/-!
# Boundary-support monotonicity

This derives

`support (boundary F) ⊆ support F`

from the primitive face-support compatibility carried by
`R2FillingGeometry`.
-/

noncomputable section

namespace Chronos
namespace Frontier
namespace R2FillingGeometry

/--
Every metric point in the support of a two-chain's boundary lies in the metric
support of that two-chain.
-/
theorem supp1_boundary_subset_supp2
    (G : R2FillingGeometry)
    (F : G.Face2 →₀ F2) :
    G.supp1 (G.boundary2 F) ⊆ G.supp2 F := by
  intro x hx
  rcases hx with ⟨edge, hEdgeBoundary, hxEdge⟩
  rcases
      G.boundary_face_support F edge hEdgeBoundary with
    ⟨face, hFace, hEdgeSubset⟩
  exact ⟨face, hFace, hEdgeSubset hxEdge⟩

end R2FillingGeometry
end Frontier
end Chronos
