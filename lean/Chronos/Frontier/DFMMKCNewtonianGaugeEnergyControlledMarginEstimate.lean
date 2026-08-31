import Chronos.Frontier.DFMMKCNewtonianGaugeRadiusMarginGateErrorBound
import Chronos.Frontier.DFMMKCNewtonianGaugeWeightedPerturbationEnergy

namespace Chronos.Frontier

/--
The qStar-margin gate error with the coefficient-exact weighted perturbation
norm replaced by the weakest analytic perturbation control energy.
-/
noncomputable def dfmMkcNewtonianGaugeMarginPerturbationEnergyGateErrorBound
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
    (mul_le_mul_of_nonneg_right
      (mul_le_mul_of_nonneg_left hnorm hscale) (le_of_lt hden))

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
  exact hraw.trans (by
    simpa [add_comm] using
      (add_le_add_left herr
        (dfmMkcHubbleFloorCStarStar HStar * E_grav data
          + Flux_boundary data S)))

/--
Exact algebraic reduction of the remaining absorption step.  If the scaled
four-variable perturbation control energy is bounded by `kappa` times the
background gravitational energy after restoring the positive qStar-margin
denominator, then the additive perturbation error is absorbed into the
principal coefficient, changing `C_**` to `C_** + kappa` while leaving the
boundary-flux coefficient equal to one.

This theorem does not assert the absorption hypothesis; deriving it from the
linearized Einstein-matter dynamics remains the separate physical obligation.
-/
theorem dfmMkcPerturbedQLGate_le_hubbleFloor_add_absorbedEnergy
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
    (HStar qStar kappa : ℝ)
    (hfloor : DFMMKCHubbleFloor HStar x)
    (hsub : ExpandingFlatFLRWSubHubbleSphere
      S x spatiallyFlatFLRW roundSymmetrySphere B G)
    (hrestricted :
      RestrictedDFMMKCHawkingComparisonHypotheses
        data S x spatiallyFlatFLRW roundSymmetrySphere)
    (M : DFMMKCNewtonianGaugeRelativeRadiusMargin S x P qStar)
    (habsorb :
      2 * |P.epsilon| *
          dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy S x P R ≤
        kappa * S.areaRadius * (1 - qStar) * E_grav data) :
    DFMMKCPerturbedQLGate S x P ≤
      (dfmMkcHubbleFloorCStarStar HStar + kappa) * E_grav data
        + Flux_boundary data S := by
  have hraw :
      DFMMKCPerturbedCoerciveEstimate
        (dfmMkcHubbleFloorCStarStar HStar)
        (dfmMkcNewtonianGaugeMarginPerturbationEnergyGateErrorBound
          S x P R qStar)
        S x P :=
    dfmMkcPerturbedCoerciveEstimate_of_hubbleFloor_newtonianGauge_energy
      S x spatiallyFlatFLRW roundSymmetrySphere B G P A R N H
      HStar qStar hfloor hsub hrestricted M
  have hden : 0 < S.areaRadius * (1 - qStar) :=
    mul_pos S.areaRadius_pos (sub_pos.mpr M.margin_lt_one)
  have herr :
      dfmMkcNewtonianGaugeMarginPerturbationEnergyGateErrorBound
          S x P R qStar ≤
        kappa * E_grav data := by
    unfold dfmMkcNewtonianGaugeMarginPerturbationEnergyGateErrorBound
    apply (div_le_iff₀ hden).2
    simpa [mul_assoc, mul_left_comm, mul_comm] using habsorb
  unfold DFMMKCPerturbedCoerciveEstimate at hraw
  calc
    DFMMKCPerturbedQLGate S x P ≤
        dfmMkcHubbleFloorCStarStar HStar * E_grav data
          + Flux_boundary data S
          + dfmMkcNewtonianGaugeMarginPerturbationEnergyGateErrorBound
              S x P R qStar := hraw
    _ ≤ dfmMkcHubbleFloorCStarStar HStar * E_grav data
          + Flux_boundary data S
          + kappa * E_grav data := by
      simpa [add_comm] using
        (add_le_add_left herr
          (dfmMkcHubbleFloorCStarStar HStar * E_grav data
            + Flux_boundary data S))
    _ = (dfmMkcHubbleFloorCStarStar HStar + kappa) * E_grav data
          + Flux_boundary data S := by
      ring

/--
The current abstract Newtonian-gauge carrier class cannot satisfy the proposed
perturbation-energy absorption bound uniformly with any fixed real coefficient
`kappa`.  For every explicit radius margin `0 ≤ qStar < 1`, a nonzero-Hubble
background admits a lapse-only witness with `epsilon = 1` and `Psi = 0`; hence
its relative-radius perturbation is zero and satisfies the margin, while its
analytic perturbation control energy is large enough to violate the absorption
inequality strictly.

This is a no-go theorem for the present carrier hypotheses only.  It does not
rule out absorption after adding genuine linearized Einstein-matter dynamics
that constrain the lapse potential.
-/
theorem dfmMkcNewtonianGauge_currentCarrier_violates_uniform_absorption
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (hH : x.hubble ≠ 0)
    (qStar kappa : ℝ)
    (hqStar_nonnegative : 0 ≤ qStar)
    (hqStar_lt_one : qStar < 1) :
    ∃ (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
      (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P),
      DFMMKCNewtonianGaugeRelativeRadiusMargin S x P qStar ∧
        P.epsilon = 1 ∧
          kappa * S.areaRadius * (1 - qStar) * E_grav data <
            2 * |P.epsilon| *
              dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy S x P R := by
  let target : ℝ :=
    kappa * S.areaRadius * (1 - qStar) * E_grav data / 2
  let c : ℝ := x.hubble ^ 2 * S.areaRadius ^ 3
  have hc : 0 < c := by
    dsimp [c]
    exact mul_pos (sq_pos_of_ne_zero hH) (pow_pos S.areaRadius_pos 3)
  have hcne : c ≠ 0 := ne_of_gt hc
  let phi : ℝ := (|target| + 1) / c
  let P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x := {
    epsilon := 1
    epsilon_abs_le_one := by norm_num
    waveNumberSquared := 0
    waveNumberSquared_nonnegative := by norm_num
    newtonianLapsePotential := phi
    newtonianSpatialPotential := 0
    deltaScalarField := 0
    deltaScalarFieldPrime := 0
    deltaPhaseField := 0
    deltaPhaseFieldPrime := 0
    deltaTemporalVector := 0
    deltaLongitudinalVector := 0
    deltaMatterDensityContrast := 0
    matterVelocityDivergence := 0
    areaRadiusCorrection := 0
    outgoingExpansionCorrection := 0
    ingoingExpansionCorrection := 0
    arealGradientNormSqCorrection := 0
    perturbedAreaRadius := S.areaRadius
    perturbedOutgoingExpansion := 0
    perturbedIngoingExpansion := 0
    perturbedHawkingMass := 0
    perturbedArealGradientNormSq := 0
    perturbedMisnerSharpMass := 0
    perturbedAreaRadius_eq := by simp
    perturbedAreaRadius_pos := S.areaRadius_pos
  }
  let F : DFMMKCNewtonianGaugeSphericalPotentialField := {
    potential := fun _ _ => 0
    cosmicTimeDerivative := fun _ _ => 0
    comovingRadialDerivative := fun _ _ => 0
    hasCosmicTimeDerivative := by
      intro t χ
      simpa using (hasDerivAt_const (x := t) (c := (0 : ℝ)))
    hasComovingRadialDerivative := by
      intro t χ
      simpa using (hasDerivAt_const (x := χ) (c := (0 : ℝ)))
  }
  let R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P := {
    spatialPotentialField := F
    cosmicTime := 0
    comovingRadius := 0
    arealRadius_eq := by simp
  }
  let M : DFMMKCNewtonianGaugeRelativeRadiusMargin S x P qStar := {
    relative_le_margin := by
      simpa [dfmMkcNewtonianGaugeRelativeRadiusPerturbation, P] using
        hqStar_nonnegative
    margin_lt_one := hqStar_lt_one
  }
  refine ⟨P, R, M, ?_, ?_⟩
  · rfl
  · have hlower :=
      dfmMkcNewtonianGauge_abs_lapseTerm_le_controlEnergy S x P R
    have hscale : c * phi = |target| + 1 := by
      dsimp [phi]
      field_simp [hcne]
    have hnonneg : 0 ≤ |target| + 1 := by positivity
    have hlapse :
        |-x.hubble ^ 2 * S.areaRadius ^ 3 * P.newtonianLapsePotential| =
          |target| + 1 := by
      change |-x.hubble ^ 2 * S.areaRadius ^ 3 * phi| = |target| + 1
      rw [show -x.hubble ^ 2 * S.areaRadius ^ 3 * phi = -(c * phi) by
        dsimp [c]
        ring]
      rw [abs_neg, hscale, abs_of_nonneg hnonneg]
    rw [hlapse] at hlower
    have htarget : target < |target| + 1 := by
      have hle : target ≤ |target| := le_abs_self target
      linarith
    have henergy :
        target <
          dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy S x P R :=
      lt_of_lt_of_le htarget hlower
    have hscaled :
        kappa * S.areaRadius * (1 - qStar) * E_grav data <
          2 * dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy S x P R := by
      dsimp [target] at henergy
      linarith
    simpa [P] using hscaled

end Chronos.Frontier
