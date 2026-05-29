import Chronos.Frontier.YtRGravityElasticObservablePrediction

namespace Chronos.Frontier

inductive YtRGravityElasticStandardGRBaselineKind where
  | standardOrbitDrift
  | standardLensingShift
  | standardRotationCurveCorrection
  | standardGravitationalWavePhaseShift
deriving DecidableEq, Repr

def YtRGravityElasticObservableKind.standardGRBaseline :
    YtRGravityElasticObservableKind →
    YtRGravityElasticStandardGRBaselineKind
  | .orbitDrift => .standardOrbitDrift
  | .lensingShift => .standardLensingShift
  | .rotationCurveCorrection => .standardRotationCurveCorrection
  | .gravitationalWavePhaseShift => .standardGravitationalWavePhaseShift

def YtRGravityElasticStandardGRComparisonMatches
    (obs : YtRGravityElasticObservableKind)
    (baseline : YtRGravityElasticStandardGRBaselineKind) : Prop :=
  obs.standardGRBaseline = baseline

structure YtRGravityElasticStandardGRComparison where
  observablePrediction : YtRGravityElasticObservablePrediction
  standardGRBaseline : YtRGravityElasticStandardGRBaselineKind
  baselineMatchesObservable :
    YtRGravityElasticStandardGRComparisonMatches
      observablePrediction.observable
      standardGRBaseline

def YtRMetricElasticLensingStandardGRComparison :
    YtRGravityElasticStandardGRComparison where
  observablePrediction := YtRMetricElasticLensingObservablePrediction
  standardGRBaseline := YtRGravityElasticStandardGRBaselineKind.standardLensingShift
  baselineMatchesObservable := rfl

def YtRMetricElasticWavePhaseStandardGRComparison :
    YtRGravityElasticStandardGRComparison where
  observablePrediction := YtRMetricElasticWavePhaseObservablePrediction
  standardGRBaseline := YtRGravityElasticStandardGRBaselineKind.standardGravitationalWavePhaseShift
  baselineMatchesObservable := rfl

def YtRTidalRestoringOrbitDriftStandardGRComparison :
    YtRGravityElasticStandardGRComparison where
  observablePrediction := YtRTidalRestoringOrbitDriftObservablePrediction
  standardGRBaseline := YtRGravityElasticStandardGRBaselineKind.standardOrbitDrift
  baselineMatchesObservable := rfl

def YtRTidalRestoringRotationCurveStandardGRComparison :
    YtRGravityElasticStandardGRComparison where
  observablePrediction := YtRTidalRestoringRotationCurveObservablePrediction
  standardGRBaseline := YtRGravityElasticStandardGRBaselineKind.standardRotationCurveCorrection
  baselineMatchesObservable := rfl

def YtRTidalRestoringWavePhaseStandardGRComparison :
    YtRGravityElasticStandardGRComparison where
  observablePrediction := YtRTidalRestoringWavePhaseObservablePrediction
  standardGRBaseline := YtRGravityElasticStandardGRBaselineKind.standardGravitationalWavePhaseShift
  baselineMatchesObservable := rfl

theorem ytr_gravity_elastic_standard_gr_comparison_has_observable_prediction
    (C : YtRGravityElasticStandardGRComparison) :
    C.observablePrediction.observable.isConcrete = true :=
  C.observablePrediction.observableIsConcrete

theorem ytr_gravity_elastic_standard_gr_comparison_has_serious_law
    (C : YtRGravityElasticStandardGRComparison) :
    C.observablePrediction.selectionGate.selectedLaw.isSerious = true :=
  C.observablePrediction.selectionGate.selectedLawIsSerious

theorem ytr_gravity_elastic_standard_gr_comparison_matches_baseline
    (C : YtRGravityElasticStandardGRComparison) :
    YtRGravityElasticStandardGRComparisonMatches
      C.observablePrediction.observable
      C.standardGRBaseline :=
  C.baselineMatchesObservable

end Chronos.Frontier
