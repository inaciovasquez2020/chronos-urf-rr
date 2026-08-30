import Chronos.Frontier.DFMMKCNewtonianGaugePerturbedCoerciveEstimate

namespace Chronos.Frontier

/--
Closed first-order Hawking-mass variation after substituting the spherical
Newtonian-gauge areal-radius and null-expansion corrections into the already
proved differential of the round-sphere Hawking formula.
-/
noncomputable def dfmMkcNewtonianGaugeClosedHawkingMassFirstVariation
    (areaRadius hubble lapsePotential spatialPotential
      spatialPotentialCosmicTimeDerivative
      spatialPotentialPhysicalRadialDerivative : ℝ) : ℝ :=
  areaRadius ^ 2 * spatialPotentialPhysicalRadialDerivative
    - hubble * areaRadius ^ 3 * spatialPotentialCosmicTimeDerivative
    - hubble ^ 2 * areaRadius ^ 3 * lapsePotential
    - (3 / 2 : ℝ) * hubble ^ 2 * areaRadius ^ 3 * spatialPotential

/--
The field-derived Newtonian corrections collapse the abstract Hawking first
variation to the four-term closed form

`R^2 D_r Psi - H R^3 PsiDot - H^2 R^3 Phi - (3/2) H^2 R^3 Psi`.

The apparent `Psi / R` pieces in the two null-expansion corrections cancel.
-/
theorem sphericalHawkingMassFirstVariation_eq_newtonianGaugeClosedForm
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
      S x P A R.toSphericalPotentialDerivatives) :
    sphericalHawkingMassFirstVariation
        S.areaRadius B.outgoingExpansion B.ingoingExpansion
        P.areaRadiusCorrection P.outgoingExpansionCorrection
        P.ingoingExpansionCorrection =
      dfmMkcNewtonianGaugeClosedHawkingMassFirstVariation
        S.areaRadius x.hubble P.newtonianLapsePotential
        (R.spatialPotentialField.potential R.cosmicTime R.comovingRadius)
        R.toSphericalPotentialDerivatives.cosmicTimeDerivative
        R.toSphericalPotentialDerivatives.physicalRadialDerivative := by
  rw [A.areaRadiusCorrection_eq,
    N.outgoingExpansionCorrection_eq,
    N.ingoingExpansionCorrection_eq,
    G.outgoing_eq, G.ingoing_eq,
    dfmMkcNewtonianGaugeOutgoingExpansionCorrection_eq,
    dfmMkcNewtonianGaugeIngoingExpansionCorrection_eq,
    R.spatialPotential_eq]
  unfold sphericalHawkingMassFirstVariation
    dfmMkcNewtonianGaugeClosedHawkingMassFirstVariation
    dfmMkcNewtonianGaugeAreaRadiusCorrection
    normalizedSphericalOutgoingExpansion
    normalizedSphericalIngoingExpansion
  field_simp [ne_of_gt S.areaRadius_pos]
  <;> ring

/--
Coefficient-exact weighted L1 control for the four Newtonian perturbation terms
that actually occur in the gate numerator `delta m_H + m_H Psi`.

No scalar/vector/matter perturbation slot absent from that numerator is added,
and the `Psi` coefficient is combined exactly with the background Hawking mass
rather than bounded twice.
-/
noncomputable def dfmMkcNewtonianGaugeGateWeightedPerturbationNorm
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) : ℝ :=
  |S.areaRadius ^ 2 *
      R.toSphericalPotentialDerivatives.physicalRadialDerivative|
    + |-x.hubble * S.areaRadius ^ 3 *
        R.toSphericalPotentialDerivatives.cosmicTimeDerivative|
    + |-x.hubble ^ 2 * S.areaRadius ^ 3 * P.newtonianLapsePotential|
    + |(S.hawkingMass -
          (3 / 2 : ℝ) * x.hubble ^ 2 * S.areaRadius ^ 3) *
        (R.spatialPotentialField.potential R.cosmicTime R.comovingRadius)|

/-- The coefficient-exact weighted perturbation norm is nonnegative. -/
theorem dfmMkcNewtonianGaugeGateWeightedPerturbationNorm_nonnegative
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) :
    0 ≤ dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R := by
  unfold dfmMkcNewtonianGaugeGateWeightedPerturbationNorm
  positivity

/--
After the closed-form substitution, the exact gate numerator is bounded by the
coefficient-exact four-term weighted perturbation norm.
-/
theorem abs_hawkingVariation_add_massPsi_le_weightedPerturbationNorm
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
      S x P A R.toSphericalPotentialDerivatives) :
    |sphericalHawkingMassFirstVariation
          S.areaRadius B.outgoingExpansion B.ingoingExpansion
          P.areaRadiusCorrection P.outgoingExpansionCorrection
          P.ingoingExpansionCorrection
        + S.hawkingMass * P.newtonianSpatialPotential| ≤
      dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R := by
  rw [sphericalHawkingMassFirstVariation_eq_newtonianGaugeClosedForm
    S x spatiallyFlatFLRW roundSymmetrySphere B G P A R N]
  rw [R.spatialPotential_eq]
  let a : ℝ := S.areaRadius ^ 2 *
    R.toSphericalPotentialDerivatives.physicalRadialDerivative
  let b : ℝ := -x.hubble * S.areaRadius ^ 3 *
    R.toSphericalPotentialDerivatives.cosmicTimeDerivative
  let c : ℝ := -x.hubble ^ 2 * S.areaRadius ^ 3 * P.newtonianLapsePotential
  let d : ℝ :=
    (S.hawkingMass -
      (3 / 2 : ℝ) * x.hubble ^ 2 * S.areaRadius ^ 3) *
      (R.spatialPotentialField.potential R.cosmicTime R.comovingRadius)
  have hrepr :
      dfmMkcNewtonianGaugeClosedHawkingMassFirstVariation
          S.areaRadius x.hubble P.newtonianLapsePotential
          (R.spatialPotentialField.potential R.cosmicTime R.comovingRadius)
          R.toSphericalPotentialDerivatives.cosmicTimeDerivative
          R.toSphericalPotentialDerivatives.physicalRadialDerivative
        + S.hawkingMass *
          (R.spatialPotentialField.potential R.cosmicTime R.comovingRadius) =
        a + b + c + d := by
    dsimp [a, b, c, d]
    unfold dfmMkcNewtonianGaugeClosedHawkingMassFirstVariation
    ring
  rw [hrepr]
  calc
    |a + b + c + d| ≤ |a + b + c| + |d| := abs_add_le _ _
    _ ≤ (|a + b| + |c|) + |d| := by
      exact add_le_add_right (abs_add_le _ _) _
    _ ≤ ((|a| + |b|) + |c|) + |d| := by
      exact add_le_add_right (add_le_add_right (abs_add _ _) _) _
    _ = dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R := by
      rfl

/--
Norm-based gate error.  The multiplicative factor is the exact positive
perturbed-radius factor `2 |epsilon| / R_epsilon`; no additional denominator
loss is introduced.
-/
def dfmMkcNewtonianGaugeWeightedGateErrorBound
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) : ℝ :=
  2 * |P.epsilon| *
      dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R /
    P.perturbedAreaRadius

/--
The explicit first-order Newtonian gate stability error is bounded by the
coefficient-exact weighted perturbation norm.
-/
theorem dfmMkcNewtonianGaugeFirstOrderGateStabilityError_le_weightedBound
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
      S x P A R.toSphericalPotentialDerivatives) :
    dfmMkcNewtonianGaugeFirstOrderGateStabilityError
        S x roundSymmetrySphere B P ≤
      dfmMkcNewtonianGaugeWeightedGateErrorBound S x P R := by
  have hnum :=
    abs_hawkingVariation_add_massPsi_le_weightedPerturbationNorm
      S x spatiallyFlatFLRW roundSymmetrySphere B G P A R N
  have hRadius :
      P.perturbedAreaRadius =
        S.areaRadius * (1 - P.epsilon * P.newtonianSpatialPotential) :=
    perturbedAreaRadius_eq_newtonianSpatialPotential S x P A
  unfold dfmMkcNewtonianGaugeFirstOrderGateStabilityError
    dfmMkcNewtonianGaugeFirstOrderGateCorrection
    dfmMkcNewtonianGaugeWeightedGateErrorBound
  rw [← hRadius]
  rw [abs_div, abs_mul, abs_mul]
  simp only [abs_of_nonneg (show 0 ≤ (2 : ℝ) by norm_num),
    abs_of_pos P.perturbedAreaRadius_pos]
  apply (div_le_div_iff₀ P.perturbedAreaRadius_pos).2
  exact mul_le_mul_of_nonneg_left hnum
    (mul_nonneg (by norm_num) (abs_nonneg P.epsilon))

/--
`C_**` propagation with the explicit rational gate error replaced by the
field-derived weighted perturbation norm bound.  The principal background
coefficient is unchanged.
-/
theorem dfmMkcPerturbedCoerciveEstimate_of_hubbleFloor_newtonianGauge_weightedNorm
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
    (HStar : ℝ)
    (hfloor : DFMMKCHubbleFloor HStar x)
    (hsub : ExpandingFlatFLRWSubHubbleSphere
      S x spatiallyFlatFLRW roundSymmetrySphere B G)
    (hrestricted :
      RestrictedDFMMKCHawkingComparisonHypotheses
        data S x spatiallyFlatFLRW roundSymmetrySphere)
    (hsmall :
      dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P < 1) :
    DFMMKCPerturbedCoerciveEstimate
      (dfmMkcHubbleFloorCStarStar HStar)
      (dfmMkcNewtonianGaugeWeightedGateErrorBound S x P R)
      S x P := by
  have hraw :
      DFMMKCPerturbedCoerciveEstimate
        (dfmMkcHubbleFloorCStarStar HStar)
        (dfmMkcNewtonianGaugeFirstOrderGateStabilityError
          S x roundSymmetrySphere B P)
        S x P :=
    dfmMkcPerturbedCoerciveEstimate_of_hubbleFloor_newtonianGauge
      S x spatiallyFlatFLRW roundSymmetrySphere B G P A
      R.toSphericalPotentialDerivatives N H HStar hfloor hsub hrestricted hsmall
  have herr :
      dfmMkcNewtonianGaugeFirstOrderGateStabilityError
          S x roundSymmetrySphere B P ≤
        dfmMkcNewtonianGaugeWeightedGateErrorBound S x P R :=
    dfmMkcNewtonianGaugeFirstOrderGateStabilityError_le_weightedBound
      S x spatiallyFlatFLRW roundSymmetrySphere B G P A R N
  unfold DFMMKCPerturbedCoerciveEstimate at hraw ⊢
  exact hraw.trans
    (add_le_add_left herr
      (dfmMkcHubbleFloorCStarStar HStar * E_grav data
        + Flux_boundary data S))

end Chronos.Frontier