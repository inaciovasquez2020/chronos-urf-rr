import Chronos.Frontier.GravityRecoveryObligationSurfaces

namespace Chronos
namespace Frontier

theorem gravity_curvature_neighbor_nontrivial_identity
    (C : NontrivialCurvatureNeighborGeometrySurface)
    (h : ∃ x y : C.Point, C.neighbor x y ∧ x ≠ y) :
    ∃ x y : C.Point, C.neighbor x y ∧ x ≠ y := by
  exact h

theorem gravity_curvature_neighbor_nonzero_identity
    (C : NontrivialCurvatureNeighborGeometrySurface)
    (h : ∃ x : C.Point, C.curvature x ≠ 0) :
    ∃ x : C.Point, C.curvature x ≠ 0 := by
  exact h

structure GravityCurvatureNeighborWitness where
  curvature_neighbor_surface : NontrivialCurvatureNeighborGeometrySurface
  nontrivial_neighbor_identity :
    ∃ x y : curvature_neighbor_surface.Point,
      curvature_neighbor_surface.neighbor x y ∧ x ≠ y
  nonzero_curvature_identity :
    ∃ x : curvature_neighbor_surface.Point,
      curvature_neighbor_surface.curvature x ≠ 0

theorem gravity_curvature_neighbor_witness_eliminates_nontrivial
    (W : GravityCurvatureNeighborWitness) :
    ∃ x y : W.curvature_neighbor_surface.Point,
      W.curvature_neighbor_surface.neighbor x y ∧ x ≠ y := by
  exact W.nontrivial_neighbor_identity

theorem gravity_curvature_neighbor_witness_eliminates_nonzero
    (W : GravityCurvatureNeighborWitness) :
    ∃ x : W.curvature_neighbor_surface.Point,
      W.curvature_neighbor_surface.curvature x ≠ 0 := by
  exact W.nonzero_curvature_identity

end Frontier
end Chronos
