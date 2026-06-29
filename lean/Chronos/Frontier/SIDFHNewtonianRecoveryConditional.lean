/-
  Conditional SIDFH Newtonian-recovery surface.

  This file does not derive the Newtonian limit from the SIDFH field equation.
  It isolates the exact admissible step: once the weak-field, slow-motion,
  Poisson-limit, correction-control, and force-law assumptions are supplied,
  the named `NewtonianRecovery` obligation can be produced for downstream use.
-/

import Chronos.Frontier.SIDFHFarFieldEquationBalanceConditional

namespace Chronos
namespace Frontier

universe u

/--
Minimal Newtonian-regime hypotheses needed before a modified gravity surface can
claim recovery of ordinary Newtonian gravity in the appropriate limit.
-/
structure SIDFHNewtonianRegime
    (WeakFieldMetricLimit : Prop)
    (SlowMotionLimit : Prop)
    (BaryonicPoissonLimit : Prop)
    (SIDFHCorrectionControlled : Prop)
    (PotentialForceLaw : Prop) : Prop where
  weakFieldMetricLimit : WeakFieldMetricLimit
  slowMotionLimit : SlowMotionLimit
  baryonicPoissonLimit : BaryonicPoissonLimit
  sidfhCorrectionControlled : SIDFHCorrectionControlled
  potentialForceLaw : PotentialForceLaw

/--
Explicit derivation rule for the Newtonian-recovery obligation.

This rule is not hidden inside the definition of the regime because the
repository has not yet derived the Newtonian limit from the proposed SIDFH
field equation.
-/
structure SIDFHNewtonianRecoveryRule
    (WeakFieldMetricLimit : Prop)
    (SlowMotionLimit : Prop)
    (BaryonicPoissonLimit : Prop)
    (SIDFHCorrectionControlled : Prop)
    (PotentialForceLaw : Prop)
    (NewtonianRecovery : Prop) : Prop where
  deriveNewtonianRecovery :
    WeakFieldMetricLimit →
    SlowMotionLimit →
    BaryonicPoissonLimit →
    SIDFHCorrectionControlled →
    PotentialForceLaw →
    NewtonianRecovery

/--
The bounded Newtonian theorem: supplied Newtonian-regime hypotheses and a
supplied recovery rule imply the explicit `NewtonianRecovery` obligation.
-/
theorem sidfhNewtonianRecovery_from_regime
    {WeakFieldMetricLimit : Prop}
    {SlowMotionLimit : Prop}
    {BaryonicPoissonLimit : Prop}
    {SIDFHCorrectionControlled : Prop}
    {PotentialForceLaw : Prop}
    {NewtonianRecovery : Prop}
    (hRegime :
      SIDFHNewtonianRegime
        WeakFieldMetricLimit
        SlowMotionLimit
        BaryonicPoissonLimit
        SIDFHCorrectionControlled
        PotentialForceLaw)
    (hRule :
      SIDFHNewtonianRecoveryRule
        WeakFieldMetricLimit
        SlowMotionLimit
        BaryonicPoissonLimit
        SIDFHCorrectionControlled
        PotentialForceLaw
        NewtonianRecovery) :
    NewtonianRecovery :=
  hRule.deriveNewtonianRecovery
    hRegime.weakFieldMetricLimit
    hRegime.slowMotionLimit
    hRegime.baryonicPoissonLimit
    hRegime.sidfhCorrectionControlled
    hRegime.potentialForceLaw

/--
A gravity-recovery obligation package whose Newtonian component is produced by
the explicit Newtonian regime and recovery rule.
-/
theorem sidfhGravityObligations_with_derived_newtonian_recovery
    {ι : SIDFHIndexSurface.{u}}
    {S : SIDFHSourceSurface ι}
    {Omega00WeakFieldAsymptotic : Prop}
    {FarFieldEquationBalance : Prop}
    {WeakFieldMetricLimit : Prop}
    {SlowMotionLimit : Prop}
    {BaryonicPoissonLimit : Prop}
    {SIDFHCorrectionControlled : Prop}
    {PotentialForceLaw : Prop}
    {NewtonianRecovery : Prop}
    {LensingCompatibility : Prop}
    {PerturbativeStability : Prop}
    {BoundaryMatching : Prop}
    (hConserved : ConservedSIDFHSource ι S)
    (hOmega00 : Omega00WeakFieldAsymptotic)
    (hFarField : FarFieldEquationBalance)
    (hNewtonianRegime :
      SIDFHNewtonianRegime
        WeakFieldMetricLimit
        SlowMotionLimit
        BaryonicPoissonLimit
        SIDFHCorrectionControlled
        PotentialForceLaw)
    (hNewtonianRule :
      SIDFHNewtonianRecoveryRule
        WeakFieldMetricLimit
        SlowMotionLimit
        BaryonicPoissonLimit
        SIDFHCorrectionControlled
        PotentialForceLaw
        NewtonianRecovery)
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
    farFieldEquationBalance := hFarField
    newtonianRecovery :=
      sidfhNewtonianRecovery_from_regime hNewtonianRegime hNewtonianRule
    lensingCompatibility := hLensing
    perturbativeStability := hStability
    boundaryMatching := hBoundary
  }

/--
Boundary marker: the current repository still does not derive Newtonian recovery
from the displayed SIDFH field equation.
-/
def newtonianRecoveryDerivedFromSIDFHFieldEquation : Prop :=
  False

end Frontier
end Chronos
