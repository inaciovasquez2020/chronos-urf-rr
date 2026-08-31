import Chronos.Frontier.DFMMKCNewtonianGaugeSharpGateNorm

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
noncomputable def dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy
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

/--
For every fixed background state with nonzero Hubble parameter, the current
carrier interfaces admit a lapse-only family whose analytic perturbation
control energy exceeds any prescribed real threshold.  The existential
conclusion records explicitly that the witness has `epsilon = 1`, realizes
`Psi` by the identically zero field with genuine zero derivatives, and varies
only the free Newtonian lapse potential.

Thus no finite bound depending only on the fixed background data can control
this perturbation energy without an additional dynamical Einstein-matter
hypothesis tying the lapse potential to the background energy.
-/
theorem dfmMkcNewtonianGauge_controlEnergy_unbounded_in_lapse
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (hH : x.hubble ≠ 0)
    (B : ℝ) :
    ∃ (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
      (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P),
      P.epsilon = 1 ∧
        B < dfmMkcNewtonianGaugeWeightedPerturbationControlEnergy S x P R := by
  let c : ℝ := x.hubble ^ 2 * S.areaRadius ^ 3
  have hc : 0 < c := by
    dsimp [c]
    exact mul_pos (sq_pos_of_ne_zero hH) (pow_pos S.areaRadius_pos 3)
  have hcne : c ≠ 0 := ne_of_gt hc
  let phi : ℝ := (|B| + 1) / c
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
    spatialPotential_eq := by simp [F, P]
  }
  refine ⟨P, R, ?_, ?_⟩
  · rfl
  · have hlower :=
      dfmMkcNewtonianGauge_abs_lapseTerm_le_controlEnergy S x P R
    have hscale : c * phi = |B| + 1 := by
      dsimp [phi]
      field_simp [hcne]
    have hnonneg : 0 ≤ |B| + 1 := by positivity
    have hlapse :
        |-x.hubble ^ 2 * S.areaRadius ^ 3 * P.newtonianLapsePotential| =
          |B| + 1 := by
      change |-x.hubble ^ 2 * S.areaRadius ^ 3 * phi| = |B| + 1
      rw [show -x.hubble ^ 2 * S.areaRadius ^ 3 * phi = -(c * phi) by
        dsimp [c]
        ring]
      rw [abs_neg, hscale, abs_of_nonneg hnonneg]
    rw [hlapse] at hlower
    have hB : B < |B| + 1 := by
      have hle : B ≤ |B| := le_abs_self B
      linarith
    exact lt_of_lt_of_le hB hlower

/--
A local radial profile for the scalar combination `PsiDot + H Phi`.

The current carrier evaluates that combination only at the selected surface.
The scalar `0i` Einstein equation sourced by a momentum-density *component*
acts on a spatial derivative of this combination, so a derivative-faithful
interface needs an actual local radial profile rather than a direct scalar-to-
vector-component identification.
-/
structure DFMMKCNewtonianGaugeMomentumCombinationRadialProfile
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) where
  profile : ℝ → ℝ
  radialDerivative : ℝ
  surfaceValue_eq :
    profile S.areaRadius =
      dfmMkcNewtonianGaugeMomentumCombination S x P R
  hasRadialDerivative :
    HasDerivAt profile radialDerivative S.areaRadius

/--
Gradient-faithful local scalar momentum constraint for the existing typed
matter momentum-density component.

The source coefficient remains fixed by
`DFMMKCNewtonianGaugeMomentumConstraintConvention`; no numerical gravitational
normalization is invented here.  Unlike the direct scalar source binding, this
law equates the *radial derivative* of `PsiDot + H Phi` to the selected radial
momentum-density component.
-/
structure DFMMKCNewtonianGaugeRadialMomentumConstraintLaw
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (C : DFMMKCNewtonianGaugeMomentumConstraintConvention) where
  momentumProfile :
    DFMMKCNewtonianGaugeMomentumCombinationRadialProfile S x P R
  projection : DFMMKCRadialMomentumProjection S
  gaugeFixed : data.gaugeFixed
  constraintsSatisfied : data.einsteinMatterConstraintsSatisfied
  radialDerivative_eq_radialSource :
    momentumProfile.radialDerivative =
      C.coupling * projection.source

/-- The radial momentum law exposes its fixed-convention source identity. -/
theorem dfmMkcNewtonianGauge_radialMomentumDerivative_eq_fixedRadialSource
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (C : DFMMKCNewtonianGaugeMomentumConstraintConvention)
    (L : DFMMKCNewtonianGaugeRadialMomentumConstraintLaw S x P R C) :
    L.momentumProfile.radialDerivative =
      C.coupling * L.projection.source := by
  exact L.radialDerivative_eq_radialSource

/-- The local radial profile recovers the exact gate combination at the surface. -/
theorem dfmMkcNewtonianGauge_radialMomentumProfile_surfaceValue
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (Q : DFMMKCNewtonianGaugeMomentumCombinationRadialProfile S x P R) :
    Q.profile S.areaRadius =
      dfmMkcNewtonianGaugeMomentumCombination S x P R := by
  exact Q.surfaceValue_eq

/--
Anchored interval data needed to recover the gate scalar from the radial
momentum constraint.  The radial source is a scalar realization of the selected
momentum-density projection along the interval; at the surface it is required
to agree with the already-typed local projection.  No radial source profile is
fabricated from `SelectedEinsteinMatterCauchyData` alone.
-/
structure DFMMKCNewtonianGaugeRadialMomentumRecoveryBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (C : DFMMKCNewtonianGaugeMomentumConstraintConvention)
    (L : DFMMKCNewtonianGaugeRadialMomentumConstraintLaw S x P R C) where
  anchorRadius : ℝ
  anchor_le_surface : anchorRadius ≤ S.areaRadius
  radialDerivative : ℝ → ℝ
  radialSource : ℝ → ℝ
  hasRadialDerivativeWithin :
    ∀ r ∈ Set.Icc anchorRadius S.areaRadius,
      HasDerivWithinAt L.momentumProfile.profile (radialDerivative r)
        (Set.Icc anchorRadius S.areaRadius) r
  radialDerivative_eq_source :
    ∀ r ∈ Set.Icc anchorRadius S.areaRadius,
      radialDerivative r = C.coupling * radialSource r
  surfaceSource_eq :
    radialSource S.areaRadius = L.projection.source
  sourceBound : ℝ
  sourceBound_nonnegative : 0 ≤ sourceBound
  source_abs_le :
    ∀ r ∈ Set.Ico anchorRadius S.areaRadius,
      |radialSource r| ≤ sourceBound

/-- The interval source profile is compatible with the local surface law. -/
theorem dfmMkcNewtonianGauge_radialMomentumRecovery_surfaceDerivative
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (C : DFMMKCNewtonianGaugeMomentumConstraintConvention)
    (L : DFMMKCNewtonianGaugeRadialMomentumConstraintLaw S x P R C)
    (B : DFMMKCNewtonianGaugeRadialMomentumRecoveryBinding S x P R C L) :
    B.radialDerivative S.areaRadius =
      L.momentumProfile.radialDerivative := by
  have hsurface : S.areaRadius ∈ Set.Icc B.anchorRadius S.areaRadius :=
    ⟨B.anchor_le_surface, le_rfl⟩
  calc
    B.radialDerivative S.areaRadius =
        C.coupling * B.radialSource S.areaRadius :=
      B.radialDerivative_eq_source S.areaRadius hsurface
    _ = C.coupling * L.projection.source := by rw [B.surfaceSource_eq]
    _ = L.momentumProfile.radialDerivative := by
      symm
      exact L.radialDerivative_eq_radialSource

/--
Mean-value recovery of `PsiDot + H Phi` from an anchored radial source bound.
This is the first completed scalar recovery estimate for the gradient-faithful
momentum constraint on the current carrier.
-/
theorem dfmMkcNewtonianGauge_abs_momentumCombination_le_anchor_add_sourceControl
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (C : DFMMKCNewtonianGaugeMomentumConstraintConvention)
    (L : DFMMKCNewtonianGaugeRadialMomentumConstraintLaw S x P R C)
    (B : DFMMKCNewtonianGaugeRadialMomentumRecoveryBinding S x P R C L) :
    |dfmMkcNewtonianGaugeMomentumCombination S x P R| ≤
      |L.momentumProfile.profile B.anchorRadius|
        + |C.coupling| * B.sourceBound *
            (S.areaRadius - B.anchorRadius) := by
  have hsurface : S.areaRadius ∈ Set.Icc B.anchorRadius S.areaRadius :=
    ⟨B.anchor_le_surface, le_rfl⟩
  have hbound :
      ∀ r ∈ Set.Ico B.anchorRadius S.areaRadius,
        ‖B.radialDerivative r‖ ≤ |C.coupling| * B.sourceBound := by
    intro r hr
    have hrcc : r ∈ Set.Icc B.anchorRadius S.areaRadius :=
      ⟨hr.1, le_of_lt hr.2⟩
    rw [B.radialDerivative_eq_source r hrcc, Real.norm_eq_abs, abs_mul]
    exact mul_le_mul_of_nonneg_left (B.source_abs_le r hr) (abs_nonneg _)
  have hsegment :
      ‖L.momentumProfile.profile S.areaRadius -
          L.momentumProfile.profile B.anchorRadius‖ ≤
        (|C.coupling| * B.sourceBound) *
          (S.areaRadius - B.anchorRadius) := by
    exact norm_image_sub_le_of_norm_deriv_le_segment'
      B.hasRadialDerivativeWithin hbound S.areaRadius hsurface
  have hsegmentAbs :
      |L.momentumProfile.profile S.areaRadius -
          L.momentumProfile.profile B.anchorRadius| ≤
        (|C.coupling| * B.sourceBound) *
          (S.areaRadius - B.anchorRadius) := by
    simpa only [Real.norm_eq_abs] using hsegment
  have htri :
      |L.momentumProfile.profile S.areaRadius| ≤
        |L.momentumProfile.profile B.anchorRadius|
          + |L.momentumProfile.profile S.areaRadius -
              L.momentumProfile.profile B.anchorRadius| := by
    have hdecomp :
        L.momentumProfile.profile S.areaRadius =
          L.momentumProfile.profile B.anchorRadius +
            (L.momentumProfile.profile S.areaRadius -
              L.momentumProfile.profile B.anchorRadius) := by
      ring
    calc
      |L.momentumProfile.profile S.areaRadius| =
          |L.momentumProfile.profile B.anchorRadius +
            (L.momentumProfile.profile S.areaRadius -
              L.momentumProfile.profile B.anchorRadius)| :=
        congrArg (fun y : ℝ => |y|) hdecomp
      _ ≤ |L.momentumProfile.profile B.anchorRadius| +
          |L.momentumProfile.profile S.areaRadius -
            L.momentumProfile.profile B.anchorRadius| :=
        abs_add_le
          (L.momentumProfile.profile B.anchorRadius : ℝ)
          (L.momentumProfile.profile S.areaRadius -
            L.momentumProfile.profile B.anchorRadius : ℝ)
  calc
    |dfmMkcNewtonianGaugeMomentumCombination S x P R| =
        |L.momentumProfile.profile R.arealRadius| := by
      rw [L.momentumProfile.surfaceValue_eq]
    _ ≤ |L.momentumProfile.profile B.anchorRadius|
          + |L.momentumProfile.profile R.arealRadius -
              L.momentumProfile.profile B.anchorRadius| := htri
    _ ≤ |L.momentumProfile.profile B.anchorRadius|
          + |C.coupling| * B.sourceBound *
              (R.arealRadius - B.anchorRadius) := by
      exact add_le_add_left hsegmentAbs _

/--
Finished sharp-gate middle-term estimate obtained by combining the anchored
mean-value recovery with the fixed-convention radial momentum source control.
-/
theorem dfmMkcNewtonianGauge_abs_momentumGateTerm_le_anchor_add_sourceControl
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P)
    (C : DFMMKCNewtonianGaugeMomentumConstraintConvention)
    (L : DFMMKCNewtonianGaugeRadialMomentumConstraintLaw S x P R C)
    (B : DFMMKCNewtonianGaugeRadialMomentumRecoveryBinding S x P R C L) :
    |-x.hubble * S.areaRadius ^ 3 *
        dfmMkcNewtonianGaugeMomentumCombination S x P R| ≤
      |-x.hubble * S.areaRadius ^ 3| *
        (|L.momentumProfile.profile B.anchorRadius|
          + |C.coupling| * B.sourceBound *
              (R.arealRadius - B.anchorRadius)) := by
  have hcombo :=
    dfmMkcNewtonianGauge_abs_momentumCombination_le_anchor_add_sourceControl
      S x P R C L B
  calc
    |-x.hubble * S.areaRadius ^ 3 *
        dfmMkcNewtonianGaugeMomentumCombination S x P R| =
      |-x.hubble * S.areaRadius ^ 3| *
        |dfmMkcNewtonianGaugeMomentumCombination S x P R| := by
      rw [abs_mul]
    _ ≤ |-x.hubble * S.areaRadius ^ 3| *
        (|L.momentumProfile.profile B.anchorRadius|
          + |C.coupling| * B.sourceBound *
              (R.arealRadius - B.anchorRadius)) :=
      mul_le_mul_of_nonneg_left hcombo (abs_nonneg _)

end Chronos.Frontier
