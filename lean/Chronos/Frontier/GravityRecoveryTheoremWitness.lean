import Chronos.Frontier.GravityRecoveryObligationSurfaces

namespace Chronos
namespace Frontier

theorem gravity_recovery_theorem_identity
    (R : NewtonEinsteinRecoveryTheoremSurface)
    (h :
      (∃ m : R.Model, R.newtonian_limit m) ∨
      (∃ m : R.Model, R.einstein_limit m)) :
    (∃ m : R.Model, R.newtonian_limit m) ∨
    (∃ m : R.Model, R.einstein_limit m) := by
  exact h

structure GravityRecoveryTheoremWitness where
  recovery_surface : NewtonEinsteinRecoveryTheoremSurface
  recovered_identity :
    (∃ m : recovery_surface.Model, recovery_surface.newtonian_limit m) ∨
    (∃ m : recovery_surface.Model, recovery_surface.einstein_limit m)

theorem gravity_recovery_theorem_witness_eliminates
    (W : GravityRecoveryTheoremWitness) :
    (∃ m : W.recovery_surface.Model, W.recovery_surface.newtonian_limit m) ∨
    (∃ m : W.recovery_surface.Model, W.recovery_surface.einstein_limit m) := by
  exact W.recovered_identity

end Frontier
end Chronos
