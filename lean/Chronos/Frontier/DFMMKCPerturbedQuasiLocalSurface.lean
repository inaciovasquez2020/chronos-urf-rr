import Chronos.Frontier.SphericalCompactnessNullExpansionBridgeSurface

namespace Chronos.Frontier

/--
First-order DFM-MKC quasi-local surface carrier over the already-proved
flat-FLRW spherical background layer.

The perturbation coordinates mirror the repository's Newtonian-gauge linear
sector: lapse/spatial metric potentials, scalar and longitudinal-vector modes,
matter density/velocity modes, plus the charge-reduced phase perturbation used
by the action-derived stress-energy formulas.  The geometric fields are kept
explicit because the repository does not yet derive quasi-local surface
geometry from those Newtonian-gauge perturbations.

This is a carrier only.  In particular, it does not assert a perturbed Hawking
formula, a perturbed Misner-Sharp formula, or any stability estimate.
-/
structure DFMMKCPerturbedQuasiLocalSurfaceCarrier
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (_x : RestrictedDFMMKCEnergyState) where
  epsilon : ℝ
  epsilon_abs_le_one : |epsilon| ≤ 1
  waveNumberSquared : ℝ
  waveNumberSquared_nonnegative : 0 ≤ waveNumberSquared
  newtonianLapsePotential : ℝ
  newtonianSpatialPotential : ℝ
  deltaScalarField : ℝ
  deltaScalarFieldPrime : ℝ
  deltaPhaseField : ℝ
  deltaPhaseFieldPrime : ℝ
  deltaTemporalVector : ℝ
  deltaLongitudinalVector : ℝ
  deltaMatterDensityContrast : ℝ
  matterVelocityDivergence : ℝ
  areaRadiusCorrection : ℝ
  outgoingExpansionCorrection : ℝ
  ingoingExpansionCorrection : ℝ
  arealGradientNormSqCorrection : ℝ
  perturbedAreaRadius : ℝ
  perturbedAreaRadius_eq :
    perturbedAreaRadius = S.areaRadius + epsilon * areaRadiusCorrection
  perturbedAreaRadius_pos : 0 < perturbedAreaRadius
  perturbedOutgoingExpansion : ℝ
  perturbedIngoingExpansion : ℝ
  perturbedHawkingMass : ℝ
  perturbedArealGradientNormSq : ℝ
  perturbedMisnerSharpMass : ℝ

/--
Areal-gradient scalar reconstructed from real spherical null expansions in the
fixed `g(l,n) = -2` normalization.
-/
def sphericalArealGradientNormSqFromExpansions
    (areaRadius outgoingExpansion ingoingExpansion : ℝ) : ℝ :=
  -(areaRadius ^ 2 * outgoingExpansion * ingoingExpansion / 4)

/-- First variation of `r_A^2 * theta_+ * theta_- / 4`. -/
def sphericalExpansionProductFirstVariation
    (areaRadius outgoingExpansion ingoingExpansion
      areaRadiusCorrection outgoingExpansionCorrection
      ingoingExpansionCorrection : ℝ) : ℝ :=
  areaRadius * areaRadiusCorrection * outgoingExpansion * ingoingExpansion / 2
    + areaRadius ^ 2 *
      (outgoingExpansionCorrection * ingoingExpansion
        + outgoingExpansion * ingoingExpansionCorrection) / 4

/--
First variation of the round-sphere Hawking mass
`m_H = r_A/2 + r_A^3 theta_+ theta_-/8`.
-/
def sphericalHawkingMassFirstVariation
    (areaRadius outgoingExpansion ingoingExpansion
      areaRadiusCorrection outgoingExpansionCorrection
      ingoingExpansionCorrection : ℝ) : ℝ :=
  areaRadiusCorrection / 2
    + (3 * areaRadius ^ 2 * areaRadiusCorrection *
        outgoingExpansion * ingoingExpansion
      + areaRadius ^ 3 *
        (outgoingExpansionCorrection * ingoingExpansion
          + outgoingExpansion * ingoingExpansionCorrection)) / 8

/--
First-order spherical Hawking/areal-geometry binding for a DFM-MKC perturbation.
The perturbed quantities are the linear truncations about the already-bound
round background surface.  This does not assert that the Newtonian-gauge field
variables determine the correction coefficients; that map remains a separate
geometric obligation.
-/
structure DFMMKCFirstOrderSphericalHawkingGeometryBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) where
  perturbedOutgoingExpansion_eq :
    P.perturbedOutgoingExpansion =
      B.outgoingExpansion + P.epsilon * P.outgoingExpansionCorrection
  perturbedIngoingExpansion_eq :
    P.perturbedIngoingExpansion =
      B.ingoingExpansion + P.epsilon * P.ingoingExpansionCorrection
  arealGradientNormSqCorrection_eq :
    P.arealGradientNormSqCorrection =
      -sphericalExpansionProductFirstVariation
        S.areaRadius B.outgoingExpansion B.ingoingExpansion
        P.areaRadiusCorrection P.outgoingExpansionCorrection
        P.ingoingExpansionCorrection
  perturbedArealGradientNormSq_eq :
    P.perturbedArealGradientNormSq =
      sphericalArealGradientNormSqFromExpansions
          S.areaRadius B.outgoingExpansion B.ingoingExpansion
        + P.epsilon * P.arealGradientNormSqCorrection
  perturbedHawkingMass_eq :
    P.perturbedHawkingMass =
      S.hawkingMass + P.epsilon *
        sphericalHawkingMassFirstVariation
          S.areaRadius B.outgoingExpansion B.ingoingExpansion
          P.areaRadiusCorrection P.outgoingExpansionCorrection
          P.ingoingExpansionCorrection

end Chronos.Frontier
