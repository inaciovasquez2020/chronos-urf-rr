import Chronos.Frontier.DFMMKCNewtonianGaugeGateErrorBound

namespace Chronos.Frontier

/--
The scalar Newtonian-gauge combination that occurs jointly in the exact
first-order gate numerator and in the scalar Einstein momentum constraint.
No Einstein equation is assumed here; this is only the coefficient-exact
algebraic combination already present in the gate numerator.
-/
noncomputable def dfmMkcNewtonianGaugeMomentumCombination
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
noncomputable def dfmMkcNewtonianGaugeGateSharpPerturbationNorm
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
    |a + b + d| ≤ |a + b| + |d| := abs_add_le _ _
    _ ≤ (|a| + |b|) + |d| := by
      exact add_le_add_right (abs_add_le _ _) _
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

/--
Typed surface-local binding for the scalar Newtonian-gauge momentum
combination.  It records the weakest missing dynamical interface: a chosen
surface point and spatial direction, an explicit normalization coefficient,
proof that the selected gauge and Einstein-matter constraints hold, and the
exact source identity relating `PsiDot + H Phi` to the corresponding component
of the already-typed matter momentum density.

No value or sign for `coupling` is assumed here, and no existence claim is
made for this structure.
-/
structure DFMMKCNewtonianGaugeMomentumConstraintBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) where
  surfacePoint : S.surfacePoint
  spatialDirection : Fin 3
  coupling : ℝ
  gaugeFixed : data.gaugeFixed
  constraintsSatisfied : data.einsteinMatterConstraintsSatisfied
  momentumCombination_eq_source :
    dfmMkcNewtonianGaugeMomentumCombination S x P R =
      coupling *
        data.matterMomentumDensity
          (S.inclusion surfacePoint)
          spatialDirection

/--
Once a momentum-constraint binding is supplied, the middle term of the sharp
gate norm rewrites exactly to the typed matter-momentum source.  This is only
an algebraic consequence of the binding and does not assert that such a
binding exists for the current carrier.
-/
theorem dfmMkcNewtonianGauge_abs_momentumGateTerm_eq_boundSource
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (B : DFMMKCNewtonianGaugeMomentumConstraintBinding S x P R) :
    |-x.hubble * S.areaRadius ^ 3 *
        dfmMkcNewtonianGaugeMomentumCombination S x P R| =
      |-x.hubble * S.areaRadius ^ 3 *
        (B.coupling *
          data.matterMomentumDensity
            (S.inclusion B.surfacePoint)
            B.spatialDirection)| := by
  rw [B.momentumCombination_eq_source]

/--
A momentum-constraint convention fixes the two pieces that were previously
collapsed into the free `coupling`: the source sign and normalization.  The
sign is required to be one of the two orientation conventions `+1` or `-1`.
The normalization is explicit data because the present Cauchy carrier does not
encode a Newton constant or a geometrized-unit convention.
-/
structure DFMMKCNewtonianGaugeMomentumConstraintConvention where
  sourceSign : ℝ
  normalization : ℝ
  sourceSign_fixed : sourceSign = 1 ∨ sourceSign = -1

/-- The coefficient fixed by a chosen momentum-constraint convention. -/
def DFMMKCNewtonianGaugeMomentumConstraintConvention.coupling
    (C : DFMMKCNewtonianGaugeMomentumConstraintConvention) : ℝ :=
  C.sourceSign * C.normalization

/--
Typed radial projection of the already-existing matter momentum density at a
chosen point of the admissible quasi-local surface.
-/
structure DFMMKCRadialMomentumProjection
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data) where
  surfacePoint : S.surfacePoint
  radialDirection : Fin 3

/-- Evaluate the typed matter momentum density in the selected radial direction. -/
def DFMMKCRadialMomentumProjection.source
    {data : SelectedEinsteinMatterCauchyData}
    {S : AdmissibleQuasiLocalSurface data}
    (Q : DFMMKCRadialMomentumProjection S) : ℝ :=
  data.matterMomentumDensity
    (S.inclusion Q.surfacePoint)
    Q.radialDirection

/--
Repository-native linearized Einstein-matter momentum-constraint law for the
current Newtonian-gauge carrier.  Unlike the earlier generic binding, the
coefficient is not a free field: it is fixed by an explicit sign/normalization
convention, and the source is reached through a typed radial projection.

This structure is the exact dynamical law object; constructing an instance is
still the physical Einstein-matter obligation.  No instance is fabricated from
`einsteinMatterConstraintsSatisfied` alone.
-/
structure DFMMKCNewtonianGaugeLinearizedMomentumConstraintLaw
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (C : DFMMKCNewtonianGaugeMomentumConstraintConvention) where
  projection : DFMMKCRadialMomentumProjection S
  gaugeFixed : data.gaugeFixed
  constraintsSatisfied : data.einsteinMatterConstraintsSatisfied
  momentumConstraint_eq_radialSource :
    dfmMkcNewtonianGaugeMomentumCombination S x P R =
      C.coupling * projection.source

/--
The fixed-convention law specializes canonically to the previous generic
binding, with no remaining free coefficient.
-/
def DFMMKCNewtonianGaugeLinearizedMomentumConstraintLaw.toBinding
    {data : SelectedEinsteinMatterCauchyData}
    {S : AdmissibleQuasiLocalSurface data}
    {x : RestrictedDFMMKCEnergyState}
    {P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x}
    {R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P}
    {C : DFMMKCNewtonianGaugeMomentumConstraintConvention}
    (L : DFMMKCNewtonianGaugeLinearizedMomentumConstraintLaw S x P R C) :
    DFMMKCNewtonianGaugeMomentumConstraintBinding S x P R :=
  {
    surfacePoint := L.projection.surfacePoint
    spatialDirection := L.projection.radialDirection
    coupling := C.coupling
    gaugeFixed := L.gaugeFixed
    constraintsSatisfied := L.constraintsSatisfied
    momentumCombination_eq_source := by
      simpa [DFMMKCRadialMomentumProjection.source] using
        L.momentumConstraint_eq_radialSource
  }

/--
With a fixed-convention momentum law, the gate's momentum term rewrites
exactly to the typed radial matter source.
-/
theorem dfmMkcNewtonianGauge_abs_momentumGateTerm_eq_fixedRadialSource
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (C : DFMMKCNewtonianGaugeMomentumConstraintConvention)
    (L : DFMMKCNewtonianGaugeLinearizedMomentumConstraintLaw S x P R C) :
    |-x.hubble * S.areaRadius ^ 3 *
        dfmMkcNewtonianGaugeMomentumCombination S x P R| =
      |-x.hubble * S.areaRadius ^ 3 *
        (C.coupling * L.projection.source)| := by
  rw [L.momentumConstraint_eq_radialSource]

end Chronos.Frontier