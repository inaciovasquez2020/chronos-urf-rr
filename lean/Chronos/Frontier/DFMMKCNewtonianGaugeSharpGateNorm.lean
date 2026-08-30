import Chronos.Frontier.DFMMKCNewtonianGaugeGateErrorBound

namespace Chronos.Frontier

/--
The scalar Newtonian-gauge combination that occurs jointly in the exact
first-order gate numerator and in the scalar Einstein momentum constraint.
No Einstein equation is assumed here; this is only the coefficient-exact
algebraic combination already present in the gate numerator.
-/
def dfmMkcNewtonianGaugeMomentumCombination
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) : ℝ :=
  R.toSphericalPotentialDerivatives.cosmicTimeDerivative
    + x.hubble * P.newtonianLapsePotential

/--
Sharper coefficient-exact gate norm obtained by keeping
`PsiDot + H Phi` together instead of applying the triangle inequality to its
two summands separately.
-/
def dfmMkcNewtonianGaugeGateSharpPerturbationNorm
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) : ℝ :=
  |S.areaRadius ^ 2 *
      R.toSphericalPotentialDerivatives.physicalRadialDerivative|
    + |-x.hubble * S.areaRadius ^ 3 *
        dfmMkcNewtonianGaugeMomentumCombination S x P R|
    + |(S.hawkingMass -
          (3 / 2 : ℝ) * x.hubble ^ 2 * S.areaRadius ^ 3) *
        (R.spatialPotentialField.potential R.cosmicTime R.comovingRadius)|

/-- The sharper three-term gate norm is nonnegative. -/
theorem dfmMkcNewtonianGaugeGateSharpPerturbationNorm_nonnegative
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) :
    0 ≤ dfmMkcNewtonianGaugeGateSharpPerturbationNorm S x P R := by
  unfold dfmMkcNewtonianGaugeGateSharpPerturbationNorm
  positivity

/--
The exact first-order gate numerator is controlled directly by the sharper
three-term norm, before any independent splitting of `PsiDot` and `Phi`.
-/
theorem abs_hawkingVariation_add_massPsi_le_sharpPerturbationNorm
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
      dfmMkcNewtonianGaugeGateSharpPerturbationNorm S x P R := by
  rw [sphericalHawkingMassFirstVariation_eq_newtonianGaugeClosedForm
    S x spatiallyFlatFLRW roundSymmetrySphere B G P A R N]
  rw [R.spatialPotential_eq]
  let a : ℝ := S.areaRadius ^ 2 *
    R.toSphericalPotentialDerivatives.physicalRadialDerivative
  let b : ℝ := -x.hubble * S.areaRadius ^ 3 *
    dfmMkcNewtonianGaugeMomentumCombination S x P R
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
        a + b + d := by
    dsimp [a, b, d]
    unfold dfmMkcNewtonianGaugeClosedHawkingMassFirstVariation
      dfmMkcNewtonianGaugeMomentumCombination
    ring
  rw [hrepr]
  calc
    |a + b + d| ≤ |a + b| + |d| := abs_add _ _
    _ ≤ (|a| + |b|) + |d| := by
      exact add_le_add_right (abs_add _ _) _
    _ = dfmMkcNewtonianGaugeGateSharpPerturbationNorm S x P R := by
      rfl

/--
The sharper norm never exceeds the previous four-term weighted norm.  The only
loss in the old norm is the triangle inequality that splits
`-H R^3 (PsiDot + H Phi)` into separate time-derivative and lapse terms.
-/
theorem dfmMkcNewtonianGaugeGateSharpPerturbationNorm_le_weighted
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) :
    dfmMkcNewtonianGaugeGateSharpPerturbationNorm S x P R ≤
      dfmMkcNewtonianGaugeGateWeightedPerturbationNorm S x P R := by
  have hmid :
      |-x.hubble * S.areaRadius ^ 3 *
          dfmMkcNewtonianGaugeMomentumCombination S x P R| ≤
        |-x.hubble * S.areaRadius ^ 3 *
          R.toSphericalPotentialDerivatives.cosmicTimeDerivative|
          + |-x.hubble ^ 2 * S.areaRadius ^ 3 *
            P.newtonianLapsePotential| := by
    rw [show
      -x.hubble * S.areaRadius ^ 3 *
          dfmMkcNewtonianGaugeMomentumCombination S x P R =
        (-x.hubble * S.areaRadius ^ 3 *
          R.toSphericalPotentialDerivatives.cosmicTimeDerivative)
          + (-x.hubble ^ 2 * S.areaRadius ^ 3 *
            P.newtonianLapsePotential) by
      unfold dfmMkcNewtonianGaugeMomentumCombination
      ring]
    exact abs_add _ _
  unfold dfmMkcNewtonianGaugeGateSharpPerturbationNorm
    dfmMkcNewtonianGaugeGateWeightedPerturbationNorm
  linarith

end Chronos.Frontier
