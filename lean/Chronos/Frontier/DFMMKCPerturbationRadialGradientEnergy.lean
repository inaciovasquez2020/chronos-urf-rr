import Chronos.Frontier.DFMMKCChargeReducedRadialMomentumSourceBinding

namespace Chronos.Frontier

/--
Quadratic radial gradient energy for the scalar/phase perturbation variables
appearing in the charge-reduced DFM-MKC momentum source.

This is the action-derived positive quadratic form before any comparison with
the curvature-energy carrier E_grav. It is deliberately local and makes no
Einstein-matter evolution or energy-control claim.
-/
noncomputable def dfmMkcPerturbationRadialGradientEnergy
    (x : RestrictedDFMMKCEnergyState)
    (deltaScalarFieldPrime deltaPhaseFieldPrime : ℝ) : ℝ :=
  x.alpha / (2 * x.scaleFactor ^ 2) * deltaScalarFieldPrime ^ 2
    + x.beta * x.phi ^ 2 / (2 * x.scaleFactor ^ 2) *
        deltaPhaseFieldPrime ^ 2

/-- The action-derived radial perturbation gradient energy is nonnegative. -/
theorem dfmMkcPerturbationRadialGradientEnergy_nonneg
    (x : RestrictedDFMMKCEnergyState)
    (deltaScalarFieldPrime deltaPhaseFieldPrime : ℝ) :
    0 ≤ dfmMkcPerturbationRadialGradientEnergy
      x deltaScalarFieldPrime deltaPhaseFieldPrime := by
  unfold dfmMkcPerturbationRadialGradientEnergy
  positivity

end Chronos.Frontier
