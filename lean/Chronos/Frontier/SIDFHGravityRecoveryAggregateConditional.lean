/-
  Aggregate conditional SIDFH gravity-recovery rollup.

  This file combines the existing conditional surfaces into one bounded theorem.
  It does not prove unconditional gravity recovery. It proves only that supplied
  regime hypotheses and explicit derivation rules produce the existing
  conditional gravity-recovery package with a flat-rotation-curve limit.
-/

import Chronos.Frontier.SIDFHBoundaryMatchingConditional

namespace Chronos
namespace Frontier

universe u

/--
Aggregate conditional rollup.

Given:
* an explicit conserved SIDFH source,
* an explicit Omega00 weak-field asymptotic,
* far-field regime hypotheses plus a balance rule,
* Newtonian-regime hypotheses plus a recovery rule,
* lensing-regime hypotheses plus a compatibility rule,
* perturbative-regime hypotheses plus a stability rule,
* boundary-regime hypotheses plus a matching rule,
* a circular-orbit law,
* and a flat-curve derivation rule,

the existing conditional gravity-recovery package with flat-rotation limit
follows.
-/
theorem sidfhGravityRecoveryAggregateConditional_from_regimes
    {ι : SIDFHIndexSurface.{u}}
    {S : SIDFHSourceSurface ι}
    {Omega00WeakFieldAsymptotic : Prop}
    {BaryonicSourceNegligible : Prop}
    {EinsteinTermControlled : Prop}
    {CosmologicalTermControlled : Prop}
    {HigherCurvatureTermControlled : Prop}
    {SIDFHTermLeading : Prop}
    {FarFieldEquationBalance : Prop}
    {WeakFieldMetricLimit : Prop}
    {SlowMotionLimit : Prop}
    {BaryonicPoissonLimit : Prop}
    {SIDFHCorrectionControlled : Prop}
    {PotentialForceLaw : Prop}
    {NewtonianRecovery : Prop}
    {NullPropagationLimit : Prop}
    {WeakLensingLimit : Prop}
    {MetricPotentialCompatibility : Prop}
    {DeflectionAngleLimit : Prop}
    {ObservedLensingCalibration : Prop}
    {LensingCompatibility : Prop}
    {LinearizedEquationWellPosed : Prop}
    {HyperbolicPrincipalSymbol : Prop}
    {NoGhostModes : Prop}
    {NoTachyonicModes : Prop}
    {EnergyEstimateControlled : Prop}
    {PerturbativeStability : Prop}
    {InducedMetricMatched : Prop}
    {TraceConditionMatched : Prop}
    {NormalFluxMatched : Prop}
    {SourceJumpControlled : Prop}
    {BoundaryRegularityControlled : Prop}
    {BoundaryMatching : Prop}
    {CircularOrbitLaw : Prop}
    {FlatRotationCurveLimit : Prop}
    (hConserved : ConservedSIDFHSource ι S)
    (hOmega00 : Omega00WeakFieldAsymptotic)
    (hFarFieldRegime :
      SIDFHFarFieldRegime
        BaryonicSourceNegligible
        EinsteinTermControlled
        CosmologicalTermControlled
        HigherCurvatureTermControlled
        SIDFHTermLeading)
    (hFarFieldRule :
      SIDFHFarFieldBalanceRule
        BaryonicSourceNegligible
        EinsteinTermControlled
        CosmologicalTermControlled
        HigherCurvatureTermControlled
        SIDFHTermLeading
        FarFieldEquationBalance)
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
        BoundaryMatching)
    (hCircular : CircularOrbitLaw)
    (hFlatCurveRule :
      SIDFHFlatCurveDerivationRule
        Omega00WeakFieldAsymptotic
        FarFieldEquationBalance
        CircularOrbitLaw
        FlatRotationCurveLimit) :
    SIDFHGravityRecoveryWithFlatCurveConditional ι S
      Omega00WeakFieldAsymptotic
      FarFieldEquationBalance
      NewtonianRecovery
      LensingCompatibility
      PerturbativeStability
      BoundaryMatching
      FlatRotationCurveLimit :=
  sidfhGravityRecoveryWithFlatCurveConditional_from_obligations
    ({
      conservedSource := hConserved
      omega00WeakFieldAsymptotic := hOmega00
      farFieldEquationBalance :=
        sidfhFarFieldEquationBalance_from_regime
          hFarFieldRegime
          hFarFieldRule
      newtonianRecovery :=
        sidfhNewtonianRecovery_from_regime
          hNewtonianRegime
          hNewtonianRule
      lensingCompatibility :=
        sidfhLensingCompatibility_from_regime
          hLensingRegime
          hLensingRule
      perturbativeStability :=
        sidfhPerturbativeStability_from_regime
          hPerturbativeRegime
          hPerturbativeRule
      boundaryMatching :=
        sidfhBoundaryMatching_from_regime
          hBoundaryRegime
          hBoundaryRule
    } : SIDFHGravityRecoveryObligations ι S
      Omega00WeakFieldAsymptotic
      FarFieldEquationBalance
      NewtonianRecovery
      LensingCompatibility
      PerturbativeStability
      BoundaryMatching)
    hCircular
    hFlatCurveRule

/--
Boundary marker: even after the aggregate rollup, the repository proves only a
conditional package, not an unconditional gravity theorem.
-/
def sidfhUnconditionalGravityRecoveryClosed : Prop :=
  False

end Frontier
end Chronos
