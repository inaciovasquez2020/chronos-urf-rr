import Chronos.Frontier.DFMMKCNewtonianGaugeWeightedPerturbationEnergy

namespace Chronos.Frontier

/--
Surface-local action-source binding for the charge-reduced DFM-MKC scalar
momentum potential.

The companion DFM-MKC perturbation convention is

  delta T^0_i = -partial_i q,

with

  q = (alpha * phi' * deltaPhi
      + beta * phi^2 * theta' * deltaTheta) / a^2.

Using phi' = a * phiDot, theta' = a * thetaDot, and the conserved charge

  qTheta = beta * a^3 * phi^2 * thetaDot,

the scalar potential becomes

  q = alpha * phiDot * deltaPhi / a
      + qTheta * deltaTheta / a^4.

The present Cauchy-data carrier does not specify whether
`matterMomentumDensity` is the coordinate component `delta T^0_i`, an ADM
momentum density, or an orthonormal radial component.  Therefore the radial
projection sign and positive normalization are explicit fields rather than
silently fixed.

This structure asserts no existence theorem and supplies no interval source
bound.  It only records the weakest surface-local action-to-carrier binding.
-/
structure DFMMKCChargeReducedRadialMomentumSourceBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) where
  projection : DFMMKCRadialMomentumProjection S
  deltaScalarProfile : ℝ → ℝ
  deltaPhaseProfile : ℝ → ℝ
  momentumPotentialProfile : ℝ → ℝ
  momentumPotentialRadialDerivative : ℝ
  projectionSign : ℝ
  projectionNormalization : ℝ
  projectionSign_fixed : projectionSign = 1 ∨ projectionSign = -1
  projectionNormalization_pos : 0 < projectionNormalization
  deltaScalar_surface :
    deltaScalarProfile S.areaRadius = P.deltaScalarField
  deltaPhase_surface :
    deltaPhaseProfile S.areaRadius = P.deltaPhaseField
  momentumPotential_eq :
    ∀ r,
      momentumPotentialProfile r =
        x.alpha * x.phiDot * deltaScalarProfile r / x.scaleFactor
          + x.qTheta * deltaPhaseProfile r / x.scaleFactor ^ 4
  hasMomentumPotentialRadialDerivative :
    HasDerivAt momentumPotentialProfile
      momentumPotentialRadialDerivative S.areaRadius
  projectedMatterMomentum_eq :
    projection.source =
      projectionSign * projectionNormalization *
        momentumPotentialRadialDerivative

/--
Interval extension of the charge-reduced DFM-MKC action-source identity.

This deliberately carries no `sourceBound` and no `source_abs_le` field.  It
only states that, on the same closed radial-interval geometry used by the
Newtonian-gauge recovery argument, the realized radial momentum source is the
signed, positively normalized radial derivative of the charge-reduced momentum
potential.  The derivative at the selected surface is tied back to the
surface-local binding above.
-/
structure DFMMKCChargeReducedRadialMomentumSourceIntervalBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (Q : DFMMKCChargeReducedRadialMomentumSourceBinding S x P) where
  anchorRadius : ℝ
  anchor_le_surface : anchorRadius ≤ S.areaRadius
  radialSource : ℝ → ℝ
  momentumPotentialRadialDerivative : ℝ → ℝ
  hasMomentumPotentialRadialDerivativeWithin :
    ∀ r ∈ Set.Icc anchorRadius S.areaRadius,
      HasDerivWithinAt Q.momentumPotentialProfile
        (momentumPotentialRadialDerivative r)
        (Set.Icc anchorRadius S.areaRadius) r
  radialSource_eq :
    ∀ r ∈ Set.Icc anchorRadius S.areaRadius,
      radialSource r =
        Q.projectionSign * Q.projectionNormalization *
          momentumPotentialRadialDerivative r
  surfaceDerivative_eq :
    momentumPotentialRadialDerivative S.areaRadius =
      Q.momentumPotentialRadialDerivative

/-- The interval action-source profile recovers the typed local source. -/
theorem dfmMkcChargeReducedRadialMomentumSourceIntervalBinding_surfaceSource_eq
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (Q : DFMMKCChargeReducedRadialMomentumSourceBinding S x P)
    (B : DFMMKCChargeReducedRadialMomentumSourceIntervalBinding S x P Q) :
    B.radialSource S.areaRadius = Q.projection.source := by
  have hsurface : S.areaRadius ∈ Set.Icc B.anchorRadius S.areaRadius :=
    ⟨B.anchor_le_surface, le_rfl⟩
  calc
    B.radialSource S.areaRadius =
        Q.projectionSign * Q.projectionNormalization *
          B.momentumPotentialRadialDerivative S.areaRadius :=
      B.radialSource_eq S.areaRadius hsurface
    _ = Q.projectionSign * Q.projectionNormalization *
          Q.momentumPotentialRadialDerivative := by
      rw [B.surfaceDerivative_eq]
    _ = Q.projection.source := by
      symm
      exact Q.projectedMatterMomentum_eq

/--
On the interval, taking absolute values removes the unresolved projection sign.
Thus the magnitude of the realized radial matter source is exactly the positive
projection normalization times the magnitude of the radial derivative of the
charge-reduced momentum potential.
-/
theorem dfmMkcChargeReducedRadialMomentumSourceIntervalBinding_abs_source_eq
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (Q : DFMMKCChargeReducedRadialMomentumSourceBinding S x P)
    (B : DFMMKCChargeReducedRadialMomentumSourceIntervalBinding S x P Q)
    (r : ℝ)
    (hr : r ∈ Set.Icc B.anchorRadius S.areaRadius) :
    |B.radialSource r| =
      Q.projectionNormalization * |B.momentumPotentialRadialDerivative r| := by
  rw [B.radialSource_eq r hr, abs_mul, abs_mul,
    abs_of_pos Q.projectionNormalization_pos]
  rcases Q.projectionSign_fixed with hsign | hsign
  · rw [hsign, abs_one, one_mul]
  · rw [hsign, abs_neg, abs_one, one_mul]

end Chronos.Frontier
