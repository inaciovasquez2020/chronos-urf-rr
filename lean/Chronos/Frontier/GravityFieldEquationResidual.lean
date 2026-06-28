import Chronos.Frontier.GravityRecoveryObligationSurfaces

namespace Chronos
namespace Frontier

theorem gravity_field_equation_residual_identity
    (F : GravityFieldEquationSurface)
    (h : ∀ g : F.Geometry, F.residual g = F.curvature g - F.source g) :
    ∀ g : F.Geometry, F.residual g = F.curvature g - F.source g := by
  exact h

structure GravityFieldEquationResidualWitness where
  field_surface : GravityFieldEquationSurface
  residual_identity :
    ∀ g : field_surface.Geometry,
      field_surface.residual g =
        field_surface.curvature g - field_surface.source g

theorem gravity_field_equation_residual_witness_eliminates
    (W : GravityFieldEquationResidualWitness) :
    ∀ g : W.field_surface.Geometry,
      W.field_surface.residual g =
        W.field_surface.curvature g - W.field_surface.source g := by
  exact W.residual_identity

end Frontier
end Chronos
