/-
  Conditional SIDFH bridge-divergence compatibility surface.

  This file does not derive divergence-freeness of the displayed bridge tensor.
  It isolates the exact admissible replacement for the invalid informal step:
  if shadow and bridge divergence data are supplied, and a compatibility rule
  maps those data to the total source divergence, then the conserved-source
  invariant follows.
-/

import Chronos.Frontier.SIDFHGravityRecoveryAggregateConditional

namespace Chronos
namespace Frontier

universe u

/--
A decomposed SIDFH divergence surface.

`shadowDivergence ν` represents the contribution of the shadow/extrinsic part.
`bridgeDivergence ν` represents the contribution of the bridge part.
`source.divergence ν` represents the total divergence component.
-/
structure SIDFHDecomposedDivergenceSurface
    (ι : SIDFHIndexSurface.{u}) where
  source : SIDFHSourceSurface ι
  shadowDivergence : ι.Index → Prop
  bridgeDivergence : ι.Index → Prop

/--
Explicit invariant for the shadow contribution.
-/
structure SIDFHShadowDivergenceInvariant
    (ι : SIDFHIndexSurface.{u})
    (D : SIDFHDecomposedDivergenceSurface ι) : Prop where
  shadow : ∀ ν : ι.Index, D.shadowDivergence ν

/--
Explicit invariant for the bridge contribution.

This is not derived from the displayed bridge tensor here.
-/
structure SIDFHBridgeDivergenceInvariant
    (ι : SIDFHIndexSurface.{u})
    (D : SIDFHDecomposedDivergenceSurface ι) : Prop where
  bridge : ∀ ν : ι.Index, D.bridgeDivergence ν

/--
Compatibility rule connecting decomposed divergence data to the total source
divergence.

This is the precise replacement for the previous informal cancellation claim.
-/
structure SIDFHBridgeDivergenceCompatibility
    (ι : SIDFHIndexSurface.{u})
    (D : SIDFHDecomposedDivergenceSurface ι) : Prop where
  totalFromParts :
    ∀ ν : ι.Index,
      D.shadowDivergence ν →
      D.bridgeDivergence ν →
      D.source.divergence ν

/--
If the shadow divergence invariant, bridge divergence invariant, and
compatibility rule are supplied, then the total SIDFH source is conserved.
-/
theorem conservedSIDFHSource_from_bridge_divergence_compatibility
    {ι : SIDFHIndexSurface.{u}}
    {D : SIDFHDecomposedDivergenceSurface ι}
    (hShadow : SIDFHShadowDivergenceInvariant ι D)
    (hBridge : SIDFHBridgeDivergenceInvariant ι D)
    (hCompat : SIDFHBridgeDivergenceCompatibility ι D) :
    ConservedSIDFHSource ι D.source :=
  {
    conserved := fun ν =>
      hCompat.totalFromParts ν
        (hShadow.shadow ν)
        (hBridge.bridge ν)
  }

/--
A conditional aggregate rollup whose conserved-source input is produced through
the bridge-divergence compatibility surface.
-/
theorem sidfhGravityRecoveryAggregateConditional_from_bridge_compatibility
    {ι : SIDFHIndexSurface.{u}}
    {D : SIDFHDecomposedDivergenceSurface ι}
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
    (hShadow : SIDFHShadowDivergenceInvariant ι D)
    (hBridge : SIDFHBridgeDivergenceInvariant ι D)
    (hCompat : SIDFHBridgeDivergenceCompatibility ι D)
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
    SIDFHGravityRecoveryWithFlatCurveConditional ι D.source
      Omega00WeakFieldAsymptotic
      FarFieldEquationBalance
      NewtonianRecovery
      LensingCompatibility
      PerturbativeStability
      BoundaryMatching
      FlatRotationCurveLimit :=
  sidfhGravityRecoveryAggregateConditional_from_regimes
    (conservedSIDFHSource_from_bridge_divergence_compatibility
      hShadow
      hBridge
      hCompat)
    hOmega00
    hFarFieldRegime
    hFarFieldRule
    hNewtonianRegime
    hNewtonianRule
    hLensingRegime
    hLensingRule
    hPerturbativeRegime
    hPerturbativeRule
    hBoundaryRegime
    hBoundaryRule
    hCircular
    hFlatCurveRule

/--
Boundary marker: the current repository still does not derive bridge divergence
compatibility from the displayed SIDFH bridge tensor.
-/
def bridgeDivergenceCompatibilityDerivedFromDisplayedTensor : Prop :=
  False

end Frontier
end Chronos
