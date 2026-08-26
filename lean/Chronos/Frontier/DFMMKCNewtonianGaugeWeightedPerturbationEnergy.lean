import Chronos.Frontier.DFMMKCNewtonianGaugeGateErrorBound

namespace Chronos.Frontier

/--
Weakest coefficient-exact analytic perturbation energy needed by the current
spherical Newtonian-gauge gate estimate.  It controls only the four evaluated
variables that occur after the closed Hawking-mass substitution:

`Phi`, `Psi`, `∂_t Psi`, and `D_r Psi`.

This is an analytic control quantity, not a claim of a separately conserved
stress-energy.  Its weights are exactly those already present in the proved
quasi-local gate numerator bound.
-/
def dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) : ℝ :=
  dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R

/-- The weighted perturbation control energy is nonnegative. -/
theorem dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy_nonnegative
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) :
    0 ≤ dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy S x P R := by
  unfold dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy
  exact dfmMkcNewtonianGaugeGateWeightedPerturbationNorm_nonnegative S x P R

/--
The already-proved coefficient-exact weighted perturbation norm is controlled
with constant one by the weakest analytic energy above.  Equality holds by
construction, so no unproved norm-comparison constant is introduced.
-/
theorem dfmMkcNewtonianGaugeGateWeightedPerturbationNorm_le_controlEnergy
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) :
    dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R ≤
      dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy S x P R := by
  rfl

end Chronos.Frontier
