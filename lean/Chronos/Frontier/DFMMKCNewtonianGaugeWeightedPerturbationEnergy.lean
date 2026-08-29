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

/--
The lapse-potential contribution is a necessary component of the analytic
perturbation control energy.  Consequently any future absorption estimate for
the full control energy must, in particular, control this term; no linearized
Einstein or matter equation is assumed here.
-/
theorem dfmMkcNewtonianGauge_abs_lapseTerm_le_controlEnergy
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) :
    |-x.hubble ^ 2 * S.areaRadius ^ 3 * P.newtonianLapsePotential| ≤
      dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy S x P R := by
  unfold dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy
    dfmMkcNewtonianGaugeGateWeightedPerturbationNorm
  have hrad :
      0 ≤ |S.areaRadius ^ 2 *
        R.toSphericalPotentialDerivatives.physicalRadialDerivative| :=
    abs_nonneg _
  have htime :
      0 ≤ |-x.hubble * S.areaRadius ^ 3 *
        R.toSphericalPotentialDerivatives.cosmicTimeDerivative| :=
    abs_nonneg _
  have hpsi :
      0 ≤ |(S.hawkingMass -
        (3 / 2 : ℝ) * x.hubble ^ 2 * S.areaRadius ^ 3) *
        (R.spatialPotentialField.potential R.cosmicTime R.comovingRadius)| :=
    abs_nonneg _
  linarith

end Chronos.Frontier
