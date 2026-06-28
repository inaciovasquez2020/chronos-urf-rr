import Chronos.Frontier.GravityRecoveryObligationSurfaces

namespace Chronos
namespace Frontier

theorem gravity_motion_law_identity
    (M : GravityMotionLawSurface)
    (h : ∀ s : M.State, M.action (M.step s) = M.action s) :
    ∀ s : M.State, M.action (M.step s) = M.action s := by
  exact h

structure GravityMotionLawWitness where
  motion_surface : GravityMotionLawSurface
  stationary_identity :
    ∀ s : motion_surface.State,
      motion_surface.action (motion_surface.step s) =
        motion_surface.action s

theorem gravity_motion_law_witness_eliminates
    (W : GravityMotionLawWitness) :
    ∀ s : W.motion_surface.State,
      W.motion_surface.action (W.motion_surface.step s) =
        W.motion_surface.action s := by
  exact W.stationary_identity

end Frontier
end Chronos
