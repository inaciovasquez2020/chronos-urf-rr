/-
  Conditional SIDFH lensing-compatibility surface.

  This file does not derive gravitational lensing from the SIDFH field equation.
  It isolates the exact admissible step: once null propagation, weak-lensing,
  metric-potential, deflection-angle, and observational-calibration assumptions
  are supplied, the named `LensingCompatibility` obligation can be produced for
  downstream use.
-/

import Chronos.Frontier.SIDFHNewtonianRecoveryConditional

namespace Chronos
namespace Frontier

universe u

/--
Minimal lensing-regime hypotheses needed before a modified gravity surface can
claim compatibility with weak gravitational lensing.
-/
structure SIDFHLensingRegime
    (NullPropagationLimit : Prop)
    (WeakLensingLimit : Prop)
    (MetricPotentialCompatibility : Prop)
    (DeflectionAngleLimit : Prop)
    (ObservedLensingCalibration : Prop) : Prop where
  nullPropagationLimit : NullPropagationLimit
  weakLensingLimit : WeakLensingLimit
  metricPotentialCompatibility : MetricPotentialCompatibility
  deflectionAngleLimit : DeflectionAngleLimit
  observedLensingCalibration : ObservedLensingCalibration

/--
Explicit derivation rule for the lensing-compatibility obligation.

This rule is separated from the regime hypotheses because the repository has
not yet derived lensing compatibility from the proposed SIDFH field equation.
-/
structure SIDFHLensingCompatibilityRule
    (NullPropagationLimit : Prop)
    (WeakLensingLimit : Prop)
    (MetricPotentialCompatibility : Prop)
    (DeflectionAngleLimit : Prop)
    (ObservedLensingCalibration : Prop)
    (LensingCompatibility : Prop) : Prop where
  deriveLensingCompatibility :
    NullPropagationLimit →
    WeakLensingLimit →
    MetricPotentialCompatibility →
    DeflectionAngleLimit →
    ObservedLensingCalibration →
    LensingCompatibility

/--
The bounded lensing theorem: supplied lensing-regime hypotheses and a supplied
compatibility rule imply the explicit `LensingCompatibility` obligation.
-/
theorem sidfhLensingCompatibility_from_regime
    {NullPropagationLimit : Prop}
    {WeakLensingLimit : Prop}
    {MetricPotentialCompatibility : Prop}
    {DeflectionAngleLimit : Prop}
    {ObservedLensingCalibration : Prop}
    {LensingCompatibility : Prop}
    (hRegime :
      SIDFHLensingRegime
        NullPropagationLimit
        WeakLensingLimit
        MetricPotentialCompatibility
        DeflectionAngleLimit
        ObservedLensingCalibration)
    (hRule :
      SIDFHLensingCompatibilityRule
        NullPropagationLimit
        WeakLensingLimit
        MetricPotentialCompatibility
        DeflectionAngleLimit
        ObservedLensingCalibration
        LensingCompatibility) :
    LensingCompatibility :=
  hRule.deriveLensingCompatibility
    hRegime.nullPropagationLimit
    hRegime.weakLensingLimit
    hRegime.metricPotentialCompatibility
    hRegime.deflectionAngleLimit
    hRegime.observedLensingCalibration

/--
A gravity-recovery obligation package whose lensing component is produced by
the explicit lensing regime and compatibility rule.
-/
theorem sidfhGravityObligations_with_derived_lensing_compatibility
    {ι : SIDFHIndexSurface.{u}}
    {S : SIDFHSourceSurface ι}
    {Omega00WeakFieldAsymptotic : Prop}
    {FarFieldEquationBalance : Prop}
    {NewtonianRecovery : Prop}
    {NullPropagationLimit : Prop}
    {WeakLensingLimit : Prop}
    {MetricPotentialCompatibility : Prop}
    {DeflectionAngleLimit : Prop}
    {ObservedLensingCalibration : Prop}
    {LensingCompatibility : Prop}
    {PerturbativeStability : Prop}
    {BoundaryMatching : Prop}
    (hConserved : ConservedSIDFHSource ι S)
    (hOmega00 : Omega00WeakFieldAsymptotic)
    (hFarField : FarFieldEquationBalance)
    (hNewtonian : NewtonianRecovery)
    (hLensingRegime :
      SIDFHLensingRegime
        NullPropagationLimit
        WeakLensingLimit
        MetricPotentialCompatibility
        DeflectionAngleLimit
        ObservedLensingCalibration)
    (hLensingRule :
      SIDFHLensingCompatibilityRule
        NullPropagationLimit
        WeakLensingLimit
        MetricPotentialCompatibility
        DeflectionAngleLimit
        ObservedLensingCalibration
        LensingCompatibility)
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
    farFieldEquationBalance := hFarField
    newtonianRecovery := hNewtonian
    lensingCompatibility :=
      sidfhLensingCompatibility_from_regime hLensingRegime hLensingRule
    perturbativeStability := hStability
    boundaryMatching := hBoundary
  }

/--
Boundary marker: the current repository still does not derive lensing
compatibility from the displayed SIDFH field equation.
-/
def lensingCompatibilityDerivedFromSIDFHFieldEquation : Prop :=
  False

end Frontier
end Chronos
