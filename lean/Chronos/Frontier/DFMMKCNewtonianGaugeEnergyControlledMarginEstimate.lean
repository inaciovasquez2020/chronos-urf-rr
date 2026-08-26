import Chronos.Frontier.DFMMKCNewtonianGaugeRadiusMarginGateErrorBound
import Chronos.Frontier.DFMMKCNewtonianGaugeWeightedPerturbationEnergy

namespace Chronos.Frontier

/--
The qStar-margin gate error with the coefficient-exact weighted perturbation
norm replaced by the weakest analytic perturbation control energy.
-/
def dfmMkcNewtonianGaugeMarginPerturbationEnergyGateErrorBound
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (qStar : ℝ) : ℝ :=
  2 * |P.epsilon| *
      dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy S x P R /
    (S.areaRadius * (1 - qStar))

/--
The previously verified qStar-margin weighted-norm error is controlled by the
new perturbation energy with no loss in the numerator constant.
-/
theorem dfmMkcNewtonianGaugeMarginWeightedGateErrorBound_le_energyBound
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (qStar : ℝ)
    (M : DFMMKCNewtonianGaugeRelativeRadiusMargin S x P qStar) :
    dfmMkcNewtonianGaugeMarginWeightedGateErrorBound S x P R qStar ≤
      dfmMkcNewtonianGaugeMarginPerturbationEnergyGateErrorBound
        S x P R qStar := by
  have hden : 0 < S.areaRadius * (1 - qStar) :=
    mul_pos S.areaRadius_pos (sub_pos.mpr M.margin_lt_one)
  have hnorm :
      dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R ≤
        dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy S x P R :=
    dfmMkcNewtonianGaugeGateWeightedPerturbationNorm_le_controlEnergy
      S x P R
  have hscale : 0 ≤ 2 * |P.epsilon| := by
    positivity
  unfold dfmMkcNewtonianGaugeMarginWeightedGateErrorBound
    dfmMkcNewtonianGaugeMarginPerturbationEnergyGateErrorBound
  exact (div_le_div_iff₀ hden hden).2
    (mul_le_mul_of_nonneg_left hnorm hscale)

/--
The spherical first-order DFM-MKC qStar-margin coercive estimate with its
additive perturbation term expressed entirely through the four-variable
analytic control energy.  The background coefficient C_** is unchanged.
-/
theorem dfmMkcPerturbedCoerciveEstimate_of_hubbleFloor_newtonianGauge_energy
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
      (dfmMkcNewtonianGaugeMarginPerturbationEnergyGateErrorBound
        S x P R qStar)
      S x P := by
  have hraw :
      DFMMKCPerturbedCoerciveEstimate
        (dfmMkcHubbleFloorCStarStar HStar)
        (dfmMkcNewtonianGaugeMarginWeightedGateErrorBound S x P R qStar)
        S x P :=
    dfmMkcPerturbedCoerciveEstimate_of_hubbleFloor_newtonianGauge_margin
      S x spatiallyFlatFLRW roundSymmetrySphere B G P A R N H
      HStar qStar hfloor hsub hrestricted M
  have herr :
      dfmMkcNewtonianGaugeMarginWeightedGateErrorBound S x P R qStar ≤
        dfmMkcNewtonianGaugeMarginPerturbationEnergyGateErrorBound
          S x P R qStar :=
    dfmMkcNewtonianGaugeMarginWeightedGateErrorBound_le_energyBound
      S x P R qStar M
  unfold DFMMKCPerturbedCoerciveEstimate at hraw ⊢
  exact hraw.trans
    (add_le_add_left herr
      (dfmMkcHubbleFloorCStarStar HStar * E_grav data
        + Flux_boundary data S))

end Chronos.Frontier
