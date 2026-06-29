/-
  Conditional SIDFH far-field equation-balance surface.

  This file does not prove that the SIDFH field equation has the required
  far-field balance.  It isolates the exact admissible step: once the relevant
  decay, dominance, and balance assumptions are supplied, the named
  `FarFieldEquationBalance` obligation can be produced for downstream use.
-/

import Chronos.Frontier.SIDFHOmega00FlatCurveConditional

namespace Chronos
namespace Frontier

/--
Minimal far-field hypotheses needed to justify keeping the SIDFH term while
discarding baryonic, Einstein, cosmological, and higher-curvature terms in the
rotation-curve regime.

All fields are propositions because this surface records dependency structure,
not analytic estimates.
-/
structure SIDFHFarFieldRegime
    (BaryonicSourceNegligible : Prop)
    (EinsteinTermControlled : Prop)
    (CosmologicalTermControlled : Prop)
    (HigherCurvatureTermControlled : Prop)
    (SIDFHTermLeading : Prop) : Prop where
  baryonicSourceNegligible : BaryonicSourceNegligible
  einsteinTermControlled : EinsteinTermControlled
  cosmologicalTermControlled : CosmologicalTermControlled
  higherCurvatureTermControlled : HigherCurvatureTermControlled
  sidfhTermLeading : SIDFHTermLeading

/--
Explicit derivation rule for the far-field balance obligation.

This rule is separated from the regime hypotheses because the repository has
not yet proved the analytic equation-reduction step from the proposed SIDFH
field equation.
-/
structure SIDFHFarFieldBalanceRule
    (BaryonicSourceNegligible : Prop)
    (EinsteinTermControlled : Prop)
    (CosmologicalTermControlled : Prop)
    (HigherCurvatureTermControlled : Prop)
    (SIDFHTermLeading : Prop)
    (FarFieldEquationBalance : Prop) : Prop where
  deriveBalance :
    BaryonicSourceNegligible →
    EinsteinTermControlled →
    CosmologicalTermControlled →
    HigherCurvatureTermControlled →
    SIDFHTermLeading →
    FarFieldEquationBalance

/--
The bounded far-field theorem: supplied regime hypotheses and a supplied
balance rule imply the explicit `FarFieldEquationBalance` obligation.
-/
theorem sidfhFarFieldEquationBalance_from_regime
    {BaryonicSourceNegligible : Prop}
    {EinsteinTermControlled : Prop}
    {CosmologicalTermControlled : Prop}
    {HigherCurvatureTermControlled : Prop}
    {SIDFHTermLeading : Prop}
    {FarFieldEquationBalance : Prop}
    (hRegime :
      SIDFHFarFieldRegime
        BaryonicSourceNegligible
        EinsteinTermControlled
        CosmologicalTermControlled
        HigherCurvatureTermControlled
        SIDFHTermLeading)
    (hRule :
      SIDFHFarFieldBalanceRule
        BaryonicSourceNegligible
        EinsteinTermControlled
        CosmologicalTermControlled
        HigherCurvatureTermControlled
        SIDFHTermLeading
        FarFieldEquationBalance) :
    FarFieldEquationBalance :=
  hRule.deriveBalance
    hRegime.baryonicSourceNegligible
    hRegime.einsteinTermControlled
    hRegime.cosmologicalTermControlled
    hRegime.higherCurvatureTermControlled
    hRegime.sidfhTermLeading

/--
A gravity-recovery obligation package whose far-field balance component is
produced by the explicit far-field regime and balance rule.
-/
theorem sidfhGravityObligations_with_derived_far_field_balance
    {ι : SIDFHIndexSurface}
    {S : SIDFHSourceSurface ι}
    {Omega00WeakFieldAsymptotic : Prop}
    {BaryonicSourceNegligible : Prop}
    {EinsteinTermControlled : Prop}
    {CosmologicalTermControlled : Prop}
    {HigherCurvatureTermControlled : Prop}
    {SIDFHTermLeading : Prop}
    {FarFieldEquationBalance : Prop}
    {NewtonianRecovery : Prop}
    {LensingCompatibility : Prop}
    {PerturbativeStability : Prop}
    {BoundaryMatching : Prop}
    (hConserved : ConservedSIDFHSource ι S)
    (hOmega00 : Omega00WeakFieldAsymptotic)
    (hRegime :
      SIDFHFarFieldRegime
        BaryonicSourceNegligible
        EinsteinTermControlled
        CosmologicalTermControlled
        HigherCurvatureTermControlled
        SIDFHTermLeading)
    (hRule :
      SIDFHFarFieldBalanceRule
        BaryonicSourceNegligible
        EinsteinTermControlled
        CosmologicalTermControlled
        HigherCurvatureTermControlled
        SIDFHTermLeading
        FarFieldEquationBalance)
    (hNewtonian : NewtonianRecovery)
    (hLensing : LensingCompatibility)
    (hStability : PerturbativeStability)
    (hBoundary : BoundaryMatching) :
    SIDFHGravityRecoveryObligations ι S
      Omega00WeakFieldAsymptotic
      FarFieldEquationBalance
      NewtonianRecovery
      LensingCompatibility
      PerturbativeStability
      BoundaryMatching :=
  {
    conservedSource := hConserved
    omega00WeakFieldAsymptotic := hOmega00
    farFieldEquationBalance :=
      sidfhFarFieldEquationBalance_from_regime hRegime hRule
    newtonianRecovery := hNewtonian
    lensingCompatibility := hLensing
    perturbativeStability := hStability
    boundaryMatching := hBoundary
  }

/--
Boundary marker: the current repository still does not derive the far-field
equation balance from the displayed SIDFH field equation.
-/
def farFieldEquationBalanceDerivedFromSIDFHFieldEquation : Prop :=
  False

end Frontier
end Chronos
