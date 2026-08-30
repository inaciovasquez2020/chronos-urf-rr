import Chronos.Frontier.DFMMKCNewtonianGaugeBackgroundRadiusGateErrorBound

namespace Chronos.Frontier

/--
Explicit quantitative margin for the spherical Newtonian areal-radius
perturbation.  It records exactly

`|epsilon| * |Psi| <= qStar < 1`.

No stronger pointwise or global perturbation hypothesis is included.
-/
structure DFMMKCNewtonianGaugeRelativeRadiusMargin
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (qStar : ℝ) where
  relative_le_margin :
    dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P ≤ qStar
  margin_lt_one : qStar < 1

/-- The explicit radius margin is automatically nonnegative. -/
theorem dfmMkcNewtonianGaugeRelativeRadiusMargin_nonnegative
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (qStar : ℝ)
    (M : DFMMKCNewtonianGaugeRelativeRadiusMargin S x P qStar) :
    0 ≤ qStar := by
  exact (dfmMkcNewtonianGaugeRelativeRadiusPerturbation_nonnegative
    S x P).trans M.relative_le_margin

/-- The explicit margin implies the original strict denominator smallness. -/
theorem dfmMkcNewtonianGaugeRelativeRadiusMargin_implies_small
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (qStar : ℝ)
    (M : DFMMKCNewtonianGaugeRelativeRadiusMargin S x P qStar) :
    dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P < 1 :=
  lt_of_le_of_lt M.relative_le_margin M.margin_lt_one

/--
Margin-based weighted gate error with a denominator independent of the actual
pointwise perturbation size:

`R_A * (1 - qStar)`.
-/
noncomputable def dfmMkcNewtonianGaugeMarginWeightedGateErrorBound
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (qStar : ℝ) : ℝ :=
  2 * |P.epsilon| *
      dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R /
    (S.areaRadius * (1 - qStar))

/--
The background-radius denominator `R_A (1 - |epsilon||Psi|)` is bounded below
by the explicit margin denominator `R_A (1 - qStar)`, so the corresponding
error bound increases monotonically to the margin-controlled expression.
-/
theorem dfmMkcNewtonianGaugeBackgroundRadiusBound_le_marginBound
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (qStar : ℝ)
    (M : DFMMKCNewtonianGaugeRelativeRadiusMargin S x P qStar) :
    dfmMkcNewtonianGaugeBackgroundRadiusWeightedGateErrorBound S x P R ≤
      dfmMkcNewtonianGaugeMarginWeightedGateErrorBound S x P R qStar := by
  let numerator : ℝ :=
    2 * |P.epsilon| *
      dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R
  have hnum : 0 ≤ numerator := by
    dsimp [numerator]
    exact mul_nonneg (by positivity)
      (dfmMkcNewtonianGaugeGateWeightedPerturbationNorm_nonnegative S x P R)
  have hsmall :
      dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P < 1 :=
    dfmMkcNewtonianGaugeRelativeRadiusMargin_implies_small
      S x P qStar M
  have hbackgroundPos :
      0 < S.areaRadius *
        (1 - dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P) :=
    mul_pos S.areaRadius_pos (sub_pos.mpr hsmall)
  have hmarginPos : 0 < S.areaRadius * (1 - qStar) :=
    mul_pos S.areaRadius_pos (sub_pos.mpr M.margin_lt_one)
  have hdenominator :
      S.areaRadius * (1 - qStar) ≤
        S.areaRadius *
          (1 - dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P) := by
    apply mul_le_mul_of_nonneg_left _ (le_of_lt S.areaRadius_pos)
    linarith [M.relative_le_margin]
  unfold dfmMkcNewtonianGaugeBackgroundRadiusWeightedGateErrorBound
    dfmMkcNewtonianGaugeMarginWeightedGateErrorBound
  change numerator /
      (S.areaRadius *
        (1 - dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P)) ≤
    numerator / (S.areaRadius * (1 - qStar))
  exact (div_le_div_iff₀ hbackgroundPos hmarginPos).2
    (mul_le_mul_of_nonneg_left hdenominator hnum)

/--
Direct reduction of the exact perturbed-radius weighted gate error to the fixed
margin denominator `R_A (1 - qStar)`.
-/
theorem dfmMkcNewtonianGaugeWeightedGateErrorBound_le_marginBound
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (A : DFMMKCNewtonianGaugeSphericalAreaRadiusBinding S x P)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (qStar : ℝ)
    (M : DFMMKCNewtonianGaugeRelativeRadiusMargin S x P qStar) :
    dfmMkcNewtonianGaugeWeightedGateErrorBound S x P R ≤
      dfmMkcNewtonianGaugeMarginWeightedGateErrorBound S x P R qStar := by
  have hsmall :
      dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P < 1 :=
    dfmMkcNewtonianGaugeRelativeRadiusMargin_implies_small
      S x P qStar M
  exact (dfmMkcNewtonianGaugeWeightedGateErrorBound_le_backgroundRadiusBound
      S x P A R hsmall).trans
    (dfmMkcNewtonianGaugeBackgroundRadiusBound_le_marginBound
      S x P R qStar M)

/--
The already-proved `C_**` perturbative coercive estimate with its additive error
reduced to the explicit margin denominator `R_A (1 - qStar)`.

The principal background coefficient remains unchanged; this is still a
spherical first-order Newtonian-gauge theorem.
-/
theorem dfmMkcPerturbedCoerciveEstimate_of_hubbleFloor_newtonianGauge_margin
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (G : FlatFLRWSphericalExpansionBinding
      S x spatiallyFlatFLRW roundSymmetrySphere B)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (A : DFMMKCNewtonianGaugeSphericalAreaRadiusBinding S x P)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (N : DFMMKCNewtonianGaugeSphericalNullExpansionBinding
      S x P A R.toSphericalPotentialDerivatives)
    (H : DFMMKCFirstOrderSphericalHawkingGeometryBinding
      S x roundSymmetrySphere B P)
    (HStar qStar : ℝ)
    (hfloor : DFMMKCHubbleFloor HStar x)
    (hsub : ExpandingFlatFLRWSubHubbleSphere
      S x spatiallyFlatFLRW roundSymmetrySphere B G)
    (hrestricted :
      RestrictedDFMMKCHawkingComparisonHypotheses
        data S x spatiallyFlatFLRW roundSymmetrySphere)
    (M : DFMMKCNewtonianGaugeRelativeRadiusMargin S x P qStar) :
    DFMMKCPerturbedCoerciveEstimate
      (dfmMkcHubbleFloorCStarStar HStar)
      (dfmMkcNewtonianGaugeMarginWeightedGateErrorBound S x P R qStar)
      S x P := by
  have hsmall :
      dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P < 1 :=
    dfmMkcNewtonianGaugeRelativeRadiusMargin_implies_small
      S x P qStar M
  have hraw :
      DFMMKCPerturbedCoerciveEstimate
        (dfmMkcHubbleFloorCStarStar HStar)
        (dfmMkcNewtonianGaugeWeightedGateErrorBound S x P R)
        S x P :=
    dfmMkcPerturbedCoerciveEstimate_of_hubbleFloor_newtonianGauge_weightedNorm
      S x spatiallyFlatFLRW roundSymmetrySphere B G P A R N H HStar
      hfloor hsub hrestricted hsmall
  have herr :
      dfmMkcNewtonianGaugeWeightedGateErrorBound S x P R ≤
        dfmMkcNewtonianGaugeMarginWeightedGateErrorBound S x P R qStar :=
    dfmMkcNewtonianGaugeWeightedGateErrorBound_le_marginBound
      S x P A R qStar M
  unfold DFMMKCPerturbedCoerciveEstimate at hraw ⊢
  exact hraw.trans (by
    simpa [add_comm] using
      (add_le_add_left herr
        (dfmMkcHubbleFloorCStarStar HStar * E_grav data
          + Flux_boundary data S)))

end Chronos.Frontier
