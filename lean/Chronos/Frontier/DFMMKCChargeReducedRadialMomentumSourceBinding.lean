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

end Chronos.Frontier
