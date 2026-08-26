import Chronos.Frontier.DFMMKCNewtonianGaugeGateErrorBound

namespace Chronos.Frontier

/--
Weighted first-order Newtonian gate-error bound with the perturbed areal radius
replaced by the explicit positive background-radius lower bound

`R_A * (1 - |epsilon| * |Psi|)`.

This is valid under the already-used strict relative-radius smallness condition.
-/
def dfmMkcNewtonianGaugeBackgroundRadiusWeightedGateErrorBound
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) : ℝ :=
  2 * |P.epsilon| *
      dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R /
    (S.areaRadius *
      (1 - dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P))

/--
Under `|epsilon| |Psi| < 1`, the exact perturbed-radius weighted gate bound is
controlled by the background-radius denominator
`R_A * (1 - |epsilon| |Psi|)`.
-/
theorem dfmMkcNewtonianGaugeWeightedGateErrorBound_le_backgroundRadiusBound
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (A : DFMMKCNewtonianGaugeSphericalAreaRadiusBinding S x P)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (hsmall :
      dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P < 1) :
    dfmMkcNewtonianGaugeWeightedGateErrorBound S x P R ≤
      dfmMkcNewtonianGaugeBackgroundRadiusWeightedGateErrorBound S x P R := by
  rcases perturbedAreaRadius_has_positive_newtonianLowerBound
      S x P A hsmall with ⟨hlowerPos, hlowerLe⟩
  let numerator : ℝ :=
    2 * |P.epsilon| *
      dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R
  have hnum : 0 ≤ numerator := by
    dsimp [numerator]
    positivity
  unfold dfmMkcNewtonianGaugeWeightedGateErrorBound
    dfmMkcNewtonianGaugeBackgroundRadiusWeightedGateErrorBound
  change numerator / P.perturbedAreaRadius ≤
    numerator /
      (S.areaRadius *
        (1 - dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P))
  exact (div_le_div_iff₀ P.perturbedAreaRadius_pos hlowerPos).2
    (mul_le_mul_of_nonneg_left hlowerLe hnum)

end Chronos.Frontier
