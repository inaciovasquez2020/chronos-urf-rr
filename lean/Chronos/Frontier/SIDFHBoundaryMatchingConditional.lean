/-
  Conditional SIDFH boundary-matching surface.

  This file does not derive baryonic-shadow boundary matching from the SIDFH
  action or field equation. It isolates the exact admissible step: once trace,
  normal-flux, induced-metric, source-jump, and regularity assumptions are
  supplied, the named `BoundaryMatching` obligation can be produced for
  downstream use.
-/

import Chronos.Frontier.SIDFHPerturbativeStabilityConditional

namespace Chronos
namespace Frontier

universe u

/--
Minimal boundary-regime hypotheses needed before a modified gravity surface can
claim well-posed matching across the baryonic-shadow interface.
-/
structure SIDFHBoundaryRegime
    (InducedMetricMatched : Prop)
    (TraceConditionMatched : Prop)
    (NormalFluxMatched : Prop)
    (SourceJumpControlled : Prop)
    (BoundaryRegularityControlled : Prop) : Prop where
  inducedMetricMatched : InducedMetricMatched
  traceConditionMatched : TraceConditionMatched
  normalFluxMatched : NormalFluxMatched
  sourceJumpControlled : SourceJumpControlled
  boundaryRegularityControlled : BoundaryRegularityControlled

/--
Explicit derivation rule for the boundary-matching obligation.

This rule is separated from the regime hypotheses because the repository has
not yet derived boundary matching from the proposed SIDFH dynamics.
-/
structure SIDFHBoundaryMatchingRule
    (InducedMetricMatched : Prop)
    (TraceConditionMatched : Prop)
    (NormalFluxMatched : Prop)
    (SourceJumpControlled : Prop)
    (BoundaryRegularityControlled : Prop)
    (BoundaryMatching : Prop) : Prop where
  deriveBoundaryMatching :
    InducedMetricMatched →
    TraceConditionMatched →
    NormalFluxMatched →
    SourceJumpControlled →
    BoundaryRegularityControlled →
    BoundaryMatching

/--
The bounded boundary theorem: supplied boundary-regime hypotheses and a supplied
matching rule imply the explicit `BoundaryMatching` obligation.
-/
theorem sidfhBoundaryMatching_from_regime
    {InducedMetricMatched : Prop}
    {TraceConditionMatched : Prop}
    {NormalFluxMatched : Prop}
    {SourceJumpControlled : Prop}
    {BoundaryRegularityControlled : Prop}
    {BoundaryMatching : Prop}
    (hRegime :
      SIDFHBoundaryRegime
        InducedMetricMatched
        TraceConditionMatched
        NormalFluxMatched
        SourceJumpControlled
        BoundaryRegularityControlled)
    (hRule :
      SIDFHBoundaryMatchingRule
        InducedMetricMatched
        TraceConditionMatched
        NormalFluxMatched
        SourceJumpControlled
        BoundaryRegularityControlled
        BoundaryMatching) :
    BoundaryMatching :=
  hRule.deriveBoundaryMatching
    hRegime.inducedMetricMatched
    hRegime.traceConditionMatched
    hRegime.normalFluxMatched
    hRegime.sourceJumpControlled
    hRegime.boundaryRegularityControlled

/--
A gravity-recovery obligation package whose boundary-matching component is
produced by the explicit boundary regime and matching rule.
-/
theorem sidfhGravityObligations_with_derived_boundary_matching
    {ι : SIDFHIndexSurface.{u}}
    {S : SIDFHSourceSurface ι}
    {Omega00WeakFieldAsymptotic : Prop}
    {FarFieldEquationBalance : Prop}
    {NewtonianRecovery : Prop}
    {LensingCompatibility : Prop}
    {PerturbativeStability : Prop}
    {InducedMetricMatched : Prop}
    {TraceConditionMatched : Prop}
    {NormalFluxMatched : Prop}
    {SourceJumpControlled : Prop}
    {BoundaryRegularityControlled : Prop}
    {BoundaryMatching : Prop}
    (hConserved : ConservedSIDFHSource ι S)
    (hOmega00 : Omega00WeakFieldAsymptotic)
    (hFarField : FarFieldEquationBalance)
    (hNewtonian : NewtonianRecovery)
    (hLensing : LensingCompatibility)
    (hStability : PerturbativeStability)
    (hBoundaryRegime :
      SIDFHBoundaryRegime
        InducedMetricMatched
        TraceConditionMatched
        NormalFluxMatched
        SourceJumpControlled
        BoundaryRegularityControlled)
    (hBoundaryRule :
      SIDFHBoundaryMatchingRule
        InducedMetricMatched
        TraceConditionMatched
        NormalFluxMatched
        SourceJumpControlled
        BoundaryRegularityControlled
        BoundaryMatching) :
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
    perturbativeStability := hStability
    boundaryMatching :=
      sidfhBoundaryMatching_from_regime
        hBoundaryRegime
        hBoundaryRule
  }

/--
Boundary marker: the current repository still does not derive boundary matching
from the displayed SIDFH dynamics.
-/
def boundaryMatchingDerivedFromSIDFHDynamics : Prop :=
  False

end Frontier
end Chronos
