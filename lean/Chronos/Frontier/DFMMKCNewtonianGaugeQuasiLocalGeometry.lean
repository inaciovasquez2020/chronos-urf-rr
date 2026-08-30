import Chronos.Frontier.DFMMKCPerturbedQuasiLocalSurface

namespace Chronos.Frontier

/--
Cosmic-time conformal-Newtonian convention used by the spherical perturbative
bridge:

`ds^2 = -(1 + 2 epsilon Phi) dt^2
       + a^2 (1 - 2 epsilon Psi) (dchi^2 + chi^2 dOmega^2)`.

For a background round sphere of areal radius `R`, the angular metric
coefficient is therefore `R^2 (1 - 2 epsilon Psi)` at first order.
-/
def dfmMkcNewtonianGaugeAreaRadiusCorrection
    (areaRadius spatialPotential : ℝ) : ℝ :=
  -areaRadius * spatialPotential

/--
The correction `delta R = -R Psi` has exactly the angular-metric first
variation required by the Newtonian spatial factor `1 - 2 epsilon Psi`:
`delta(R^2) = 2 R delta R = -2 R^2 Psi`.
-/
theorem dfmMkcNewtonianGaugeAreaRadiusCorrection_linearizes_angularMetric
    (areaRadius spatialPotential : ℝ) :
    2 * areaRadius *
        dfmMkcNewtonianGaugeAreaRadiusCorrection
          areaRadius spatialPotential =
      -2 * areaRadius ^ 2 * spatialPotential := by
  unfold dfmMkcNewtonianGaugeAreaRadiusCorrection
  ring

/--
Binding of the carrier's previously free areal-radius correction to the
Newtonian-gauge angular geometry.  This is spherical and first-order only.
-/
structure DFMMKCNewtonianGaugeSphericalAreaRadiusBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) where
  areaRadiusCorrection_eq :
    P.areaRadiusCorrection =
      dfmMkcNewtonianGaugeAreaRadiusCorrection
        S.areaRadius P.newtonianSpatialPotential

/--
After the Newtonian-gauge angular binding, the carrier radius is the first-order
areal radius `R_epsilon = R (1 - epsilon Psi)`.
-/
theorem perturbedAreaRadius_eq_newtonianSpatialPotential
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (A : DFMMKCNewtonianGaugeSphericalAreaRadiusBinding S x P) :
    P.perturbedAreaRadius =
      S.areaRadius * (1 - P.epsilon * P.newtonianSpatialPotential) := by
  rw [P.perturbedAreaRadius_eq, A.areaRadiusCorrection_eq]
  unfold dfmMkcNewtonianGaugeAreaRadiusCorrection
  ring

/--
Evaluated first derivatives of the Newtonian spatial potential on the selected
round sphere.  `physicalRadialDerivative` means `(1/a) partial_chi Psi` on the
flat-FLRW background, so no extra scale-factor conversion is hidden below.
-/
structure DFMMKCNewtonianGaugeSphericalPotentialDerivatives where
  cosmicTimeDerivative : ℝ
  physicalRadialDerivative : ℝ

/--
First variation of the outgoing normalized areal derivative
`l(R) = H R + 1` in the cosmic-time Newtonian gauge.
-/
def dfmMkcNewtonianGaugeOutgoingArealDerivativeCorrection
    (areaRadius hubble lapsePotential spatialPotential
      spatialPotentialCosmicTimeDerivative
      spatialPotentialPhysicalRadialDerivative : ℝ) : ℝ :=
  -areaRadius *
    (hubble * (lapsePotential + spatialPotential)
      + spatialPotentialCosmicTimeDerivative
      + spatialPotentialPhysicalRadialDerivative)

/--
First variation of the ingoing normalized areal derivative
`n(R) = H R - 1` in the same normalization.
-/
def dfmMkcNewtonianGaugeIngoingArealDerivativeCorrection
    (areaRadius hubble lapsePotential spatialPotential
      spatialPotentialCosmicTimeDerivative
      spatialPotentialPhysicalRadialDerivative : ℝ) : ℝ :=
  -areaRadius *
    (hubble * (lapsePotential + spatialPotential)
      + spatialPotentialCosmicTimeDerivative
      - spatialPotentialPhysicalRadialDerivative)

/--
First variation of a normalized spherical expansion `theta = 2 D(R) / R`.
-/
noncomputable def normalizedSphericalExpansionFirstVariation
    (areaRadius backgroundArealDerivative
      areaRadiusCorrection arealDerivativeCorrection : ℝ) : ℝ :=
  2 * arealDerivativeCorrection / areaRadius
    - normalizedSphericalOutgoingExpansion
        areaRadius backgroundArealDerivative *
      areaRadiusCorrection / areaRadius

/--
Derived outgoing null-expansion correction from the Newtonian lapse/spatial
potentials and the two evaluated derivatives of `Psi`.
-/
noncomputable def dfmMkcNewtonianGaugeOutgoingExpansionCorrection
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (D : DFMMKCNewtonianGaugeSphericalPotentialDerivatives) : ℝ :=
  normalizedSphericalExpansionFirstVariation
    S.areaRadius (x.hubble * S.areaRadius + 1)
    (dfmMkcNewtonianGaugeAreaRadiusCorrection
      S.areaRadius P.newtonianSpatialPotential)
    (dfmMkcNewtonianGaugeOutgoingArealDerivativeCorrection
      S.areaRadius x.hubble
      P.newtonianLapsePotential P.newtonianSpatialPotential
      D.cosmicTimeDerivative D.physicalRadialDerivative)

/--
Derived ingoing null-expansion correction from the same Newtonian-gauge data.
-/
noncomputable def dfmMkcNewtonianGaugeIngoingExpansionCorrection
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (D : DFMMKCNewtonianGaugeSphericalPotentialDerivatives) : ℝ :=
  normalizedSphericalExpansionFirstVariation
    S.areaRadius (x.hubble * S.areaRadius - 1)
    (dfmMkcNewtonianGaugeAreaRadiusCorrection
      S.areaRadius P.newtonianSpatialPotential)
    (dfmMkcNewtonianGaugeIngoingArealDerivativeCorrection
      S.areaRadius x.hubble
      P.newtonianLapsePotential P.newtonianSpatialPotential
      D.cosmicTimeDerivative D.physicalRadialDerivative)

/-- Closed first-order formula for the outgoing expansion correction. -/
theorem dfmMkcNewtonianGaugeOutgoingExpansionCorrection_eq
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (D : DFMMKCNewtonianGaugeSphericalPotentialDerivatives) :
    dfmMkcNewtonianGaugeOutgoingExpansionCorrection S x P D =
      -2 *
        (x.hubble * P.newtonianLapsePotential
          + D.cosmicTimeDerivative
          + D.physicalRadialDerivative
          - P.newtonianSpatialPotential / S.areaRadius) := by
  unfold dfmMkcNewtonianGaugeOutgoingExpansionCorrection
    normalizedSphericalExpansionFirstVariation
    dfmMkcNewtonianGaugeAreaRadiusCorrection
    dfmMkcNewtonianGaugeOutgoingArealDerivativeCorrection
    normalizedSphericalOutgoingExpansion
  field_simp [ne_of_gt S.areaRadius_pos]
  <;> ring

/-- Closed first-order formula for the ingoing expansion correction. -/
theorem dfmMkcNewtonianGaugeIngoingExpansionCorrection_eq
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (D : DFMMKCNewtonianGaugeSphericalPotentialDerivatives) :
    dfmMkcNewtonianGaugeIngoingExpansionCorrection S x P D =
      -2 *
        (x.hubble * P.newtonianLapsePotential
          + D.cosmicTimeDerivative
          - D.physicalRadialDerivative
          + P.newtonianSpatialPotential / S.areaRadius) := by
  unfold dfmMkcNewtonianGaugeIngoingExpansionCorrection
    normalizedSphericalExpansionFirstVariation
    dfmMkcNewtonianGaugeAreaRadiusCorrection
    dfmMkcNewtonianGaugeIngoingArealDerivativeCorrection
    normalizedSphericalOutgoingExpansion
  field_simp [ne_of_gt S.areaRadius_pos]
  <;> ring

/--
Binding of the carrier's two previously free null-expansion corrections to the
normalized Newtonian-gauge first variations above.
-/
structure DFMMKCNewtonianGaugeSphericalNullExpansionBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (_A : DFMMKCNewtonianGaugeSphericalAreaRadiusBinding S x P)
    (D : DFMMKCNewtonianGaugeSphericalPotentialDerivatives) where
  outgoingExpansionCorrection_eq :
    P.outgoingExpansionCorrection =
      dfmMkcNewtonianGaugeOutgoingExpansionCorrection S x P D
  ingoingExpansionCorrection_eq :
    P.ingoingExpansionCorrection =
      dfmMkcNewtonianGaugeIngoingExpansionCorrection S x P D

/--
Actual spherical Newtonian spatial-potential field `Psi(t, chi)` together with
its genuine one-variable derivatives in cosmic time and comoving radius.
The derivative witnesses use Mathlib's `HasDerivAt`, so the derivative values
below are no longer unconstrained scalar slots.
-/
structure DFMMKCNewtonianGaugeSphericalPotentialField where
  potential : ℝ → ℝ → ℝ
  cosmicTimeDerivative : ℝ → ℝ → ℝ
  comovingRadialDerivative : ℝ → ℝ → ℝ
  hasCosmicTimeDerivative :
    ∀ t chi,
      HasDerivAt
        (fun tau => potential tau chi)
        (cosmicTimeDerivative t chi) t
  hasComovingRadialDerivative :
    ∀ t chi,
      HasDerivAt
        (fun xi => potential t xi)
        (comovingRadialDerivative t chi) chi

/--
Physical radial derivative on the flat-FLRW background:
`D_r Psi = a^-1 partial_chi Psi`.
-/
def DFMMKCNewtonianGaugeSphericalPotentialField.physicalRadialDerivativeAt
    (F : DFMMKCNewtonianGaugeSphericalPotentialField)
    (x : RestrictedDFMMKCEnergyState)
    (t chi : ℝ) : ℝ :=
  F.comovingRadialDerivative t chi / x.scaleFactor

/--
Realization of the carrier's Newtonian spatial-potential value by an actual
spherical field evaluated at one spacetime point.  The lapse potential remains
unchanged because the current expansion formulas require its value but not its
derivatives.
-/
structure DFMMKCNewtonianGaugePerturbationFieldRealization
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) where
  spatialPotentialField : DFMMKCNewtonianGaugeSphericalPotentialField
  cosmicTime : ℝ
  comovingRadius : ℝ
  spatialPotential_eq :
    P.newtonianSpatialPotential =
      spatialPotentialField.potential cosmicTime comovingRadius

/--
The previously used evaluated derivative carrier is recovered canonically from
an actual field realization.  Its radial entry is the physical, not comoving,
derivative, matching the convention already used in the null-expansion proof.
-/
def DFMMKCNewtonianGaugePerturbationFieldRealization.toSphericalPotentialDerivatives
    {data : SelectedEinsteinMatterCauchyData}
    {S : AdmissibleQuasiLocalSurface data}
    {x : RestrictedDFMMKCEnergyState}
    {P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x}
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) :
    DFMMKCNewtonianGaugeSphericalPotentialDerivatives :=
  { cosmicTimeDerivative :=
      R.spatialPotentialField.cosmicTimeDerivative
        R.cosmicTime R.comovingRadius
    physicalRadialDerivative :=
      R.spatialPotentialField.physicalRadialDerivativeAt
        x R.cosmicTime R.comovingRadius }

/-- The recovered cosmic-time slot is the derivative of the realized field. -/
theorem DFMMKCNewtonianGaugePerturbationFieldRealization.cosmicTimeDerivative_hasDerivAt
    {data : SelectedEinsteinMatterCauchyData}
    {S : AdmissibleQuasiLocalSurface data}
    {x : RestrictedDFMMKCEnergyState}
    {P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x}
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) :
    HasDerivAt
      (fun tau => R.spatialPotentialField.potential tau R.comovingRadius)
      (R.toSphericalPotentialDerivatives.cosmicTimeDerivative)
      R.cosmicTime := by
  simpa [DFMMKCNewtonianGaugePerturbationFieldRealization.toSphericalPotentialDerivatives]
    using R.spatialPotentialField.hasCosmicTimeDerivative
      R.cosmicTime R.comovingRadius

/-- The comoving radial value underlying the recovered physical derivative is genuine. -/
theorem DFMMKCNewtonianGaugePerturbationFieldRealization.comovingRadialDerivative_hasDerivAt
    {data : SelectedEinsteinMatterCauchyData}
    {S : AdmissibleQuasiLocalSurface data}
    {x : RestrictedDFMMKCEnergyState}
    {P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x}
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) :
    HasDerivAt
      (fun xi => R.spatialPotentialField.potential R.cosmicTime xi)
      (R.spatialPotentialField.comovingRadialDerivative
        R.cosmicTime R.comovingRadius)
      R.comovingRadius :=
  R.spatialPotentialField.hasComovingRadialDerivative
    R.cosmicTime R.comovingRadius

/--
Exact recovery of the physical-radial derivative convention from the realized
field: `D_r Psi = (partial_chi Psi) / a`.
-/
theorem DFMMKCNewtonianGaugePerturbationFieldRealization.physicalRadialDerivative_eq
    {data : SelectedEinsteinMatterCauchyData}
    {S : AdmissibleQuasiLocalSurface data}
    {x : RestrictedDFMMKCEnergyState}
    {P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x}
    (R : DFMMKCNewtonianGaugePerturbationFieldRealization S x P) :
    R.toSphericalPotentialDerivatives.physicalRadialDerivative =
      R.spatialPotentialField.comovingRadialDerivative
        R.cosmicTime R.comovingRadius / x.scaleFactor := rfl

end Chronos.Frontier
