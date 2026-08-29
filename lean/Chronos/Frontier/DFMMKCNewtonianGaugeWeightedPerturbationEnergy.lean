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
    newtonianSpatialPotentialTimeDerivative := 0
    areaRadiusCorrection := 0
    outgoingExpansionCorrection := 0
    ingoingExpansionCorrection := 0
    hawkingMassCorrection := 0
    perturbedAreaRadius := S.areaRadius
    perturbedOutgoingExpansion := 0
    perturbedIngoingExpansion := 0
    perturbedHawkingMass := 0
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
    arealRadius := 0
    spatialPotentialAtSurface := by simp [F, P]
    arealRadius_eq := by simp
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

end Chronos.Frontier
