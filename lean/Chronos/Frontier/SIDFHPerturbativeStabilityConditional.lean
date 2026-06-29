/-
  Conditional SIDFH perturbative-stability surface.

  This file does not derive perturbative stability from the SIDFH action or
  field equation. It isolates the exact admissible step: once linearization,
  hyperbolicity, no-ghost, no-tachyon, and energy-control assumptions are
  supplied, the named `PerturbativeStability` obligation can be produced for
  downstream use.
-/

import Chronos.Frontier.SIDFHLensingCompatibilityConditional

namespace Chronos
namespace Frontier

universe u

/--
Minimal perturbative-regime hypotheses needed before a modified gravity surface
can claim perturbative stability.
-/
structure SIDFHPerturbativeRegime
    (LinearizedEquationWellPosed : Prop)
    (HyperbolicPrincipalSymbol : Prop)
    (NoGhostModes : Prop)
    (NoTachyonicModes : Prop)
    (EnergyEstimateControlled : Prop) : Prop where
  linearizedEquationWellPosed : LinearizedEquationWellPosed
  hyperbolicPrincipalSymbol : HyperbolicPrincipalSymbol
  noGhostModes : NoGhostModes
  noTachyonicModes : NoTachyonicModes
  energyEstimateControlled : EnergyEstimateControlled

/--
Explicit derivation rule for the perturbative-stability obligation.

This rule is separated from the regime hypotheses because the repository has
not yet derived perturbative stability from the proposed SIDFH dynamics.
-/
structure SIDFHPerturbativeStabilityRule
    (LinearizedEquationWellPosed : Prop)
    (HyperbolicPrincipalSymbol : Prop)
    (NoGhostModes : Prop)
    (NoTachyonicModes : Prop)
    (EnergyEstimateControlled : Prop)
    (PerturbativeStability : Prop) : Prop where
  derivePerturbativeStability :
    LinearizedEquationWellPosed →
    HyperbolicPrincipalSymbol →
    NoGhostModes →
    NoTachyonicModes →
    EnergyEstimateControlled →
    PerturbativeStability

/--
The bounded stability theorem: supplied perturbative-regime hypotheses and a
supplied stability rule imply the explicit `PerturbativeStability` obligation.
-/
theorem sidfhPerturbativeStability_from_regime
    {LinearizedEquationWellPosed : Prop}
    {HyperbolicPrincipalSymbol : Prop}
    {NoGhostModes : Prop}
    {NoTachyonicModes : Prop}
    {EnergyEstimateControlled : Prop}
    {PerturbativeStability : Prop}
    (hRegime :
      SIDFHPerturbativeRegime
        LinearizedEquationWellPosed
        HyperbolicPrincipalSymbol
        NoGhostModes
        NoTachyonicModes
        EnergyEstimateControlled)
    (hRule :
      SIDFHPerturbativeStabilityRule
        LinearizedEquationWellPosed
        HyperbolicPrincipalSymbol
        NoGhostModes
        NoTachyonicModes
        EnergyEstimateControlled
        PerturbativeStability) :
    PerturbativeStability :=
  hRule.derivePerturbativeStability
    hRegime.linearizedEquationWellPosed
    hRegime.hyperbolicPrincipalSymbol
    hRegime.noGhostModes
    hRegime.noTachyonicModes
    hRegime.energyEstimateControlled

/--
A gravity-recovery obligation package whose perturbative-stability component is
produced by the explicit perturbative regime and stability rule.
-/
theorem sidfhGravityObligations_with_derived_perturbative_stability
    {ι : SIDFHIndexSurface.{u}}
    {S : SIDFHSourceSurface ι}
    {Omega00WeakFieldAsymptotic : Prop}
    {FarFieldEquationBalance : Prop}
    {NewtonianRecovery : Prop}
    {LensingCompatibility : Prop}
    {LinearizedEquationWellPosed : Prop}
    {HyperbolicPrincipalSymbol : Prop}
    {NoGhostModes : Prop}
    {NoTachyonicModes : Prop}
    {EnergyEstimateControlled : Prop}
    {PerturbativeStability : Prop}
    {BoundaryMatching : Prop}
    (hConserved : ConservedSIDFHSource ι S)
    (hOmega00 : Omega00WeakFieldAsymptotic)
    (hFarField : FarFieldEquationBalance)
    (hNewtonian : NewtonianRecovery)
    (hLensing : LensingCompatibility)
    (hPerturbativeRegime :
      SIDFHPerturbativeRegime
        LinearizedEquationWellPosed
        HyperbolicPrincipalSymbol
        NoGhostModes
        NoTachyonicModes
        EnergyEstimateControlled)
    (hPerturbativeRule :
      SIDFHPerturbativeStabilityRule
        LinearizedEquationWellPosed
        HyperbolicPrincipalSymbol
        NoGhostModes
        NoTachyonicModes
        EnergyEstimateControlled
        PerturbativeStability)
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
    farFieldEquationBalance := hFarField
    newtonianRecovery := hNewtonian
    lensingCompatibility := hLensing
    perturbativeStability :=
      sidfhPerturbativeStability_from_regime
        hPerturbativeRegime
        hPerturbativeRule
    boundaryMatching := hBoundary
  }

/--
Boundary marker: the current repository still does not derive perturbative
stability from the displayed SIDFH dynamics.
-/
def perturbativeStabilityDerivedFromSIDFHDynamics : Prop :=
  False

end Frontier
end Chronos
