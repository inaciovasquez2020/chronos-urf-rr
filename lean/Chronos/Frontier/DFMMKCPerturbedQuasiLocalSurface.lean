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

end Chronos.Frontier
