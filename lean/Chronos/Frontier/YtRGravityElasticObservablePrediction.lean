import Chronos.Frontier.YtRGravityElasticLawSelectionGate

namespace Chronos.Frontier

inductive YtRGravityElasticObservableKind where
  | orbitDrift
  | lensingShift
  | rotationCurveCorrection
  | gravitationalWavePhaseShift
deriving DecidableEq, Repr

def YtRGravityElasticObservableKind.isConcrete :
    YtRGravityElasticObservableKind → Bool
  | .orbitDrift => true
  | .lensingShift => true
  | .rotationCurveCorrection => true
  | .gravitationalWavePhaseShift => true

def YtRGravityElasticAllowedObservable
    (law : YtRGravityElasticCandidateLaw)
    (obs : YtRGravityElasticObservableKind) : Prop :=
  match law, obs with
  | .metricElastic, .lensingShift => True
  | .metricElastic, .gravitationalWavePhaseShift => True
  | .tidalRestoring, .orbitDrift => True
  | .tidalRestoring, .rotationCurveCorrection => True
  | .tidalRestoring, .gravitationalWavePhaseShift => True
  | _, _ => False

structure YtRGravityElasticObservablePrediction where
  selectionGate : YtRGravityElasticLawSelectionGate
  observable : YtRGravityElasticObservableKind
  observableIsConcrete : observable.isConcrete = true
  allowedObservable :
    YtRGravityElasticAllowedObservable selectionGate.selectedLaw observable

def YtRMetricElasticLensingObservablePrediction :
    YtRGravityElasticObservablePrediction where
  selectionGate := YtRMetricElasticLawSelectionGate
  observable := YtRGravityElasticObservableKind.lensingShift
  observableIsConcrete := rfl
  allowedObservable := trivial

def YtRMetricElasticWavePhaseObservablePrediction :
    YtRGravityElasticObservablePrediction where
  selectionGate := YtRMetricElasticLawSelectionGate
  observable := YtRGravityElasticObservableKind.gravitationalWavePhaseShift
  observableIsConcrete := rfl
  allowedObservable := trivial

def YtRTidalRestoringOrbitDriftObservablePrediction :
    YtRGravityElasticObservablePrediction where
  selectionGate := YtRTidalRestoringLawSelectionGate
  observable := YtRGravityElasticObservableKind.orbitDrift
  observableIsConcrete := rfl
  allowedObservable := trivial

def YtRTidalRestoringRotationCurveObservablePrediction :
    YtRGravityElasticObservablePrediction where
  selectionGate := YtRTidalRestoringLawSelectionGate
  observable := YtRGravityElasticObservableKind.rotationCurveCorrection
  observableIsConcrete := rfl
  allowedObservable := trivial

def YtRTidalRestoringWavePhaseObservablePrediction :
    YtRGravityElasticObservablePrediction where
  selectionGate := YtRTidalRestoringLawSelectionGate
  observable := YtRGravityElasticObservableKind.gravitationalWavePhaseShift
  observableIsConcrete := rfl
  allowedObservable := trivial

theorem ytr_gravity_elastic_observable_prediction_has_serious_law
    (P : YtRGravityElasticObservablePrediction) :
    P.selectionGate.selectedLaw.isSerious = true :=
  P.selectionGate.selectedLawIsSerious

theorem ytr_gravity_elastic_observable_prediction_is_concrete
    (P : YtRGravityElasticObservablePrediction) :
    P.observable.isConcrete = true :=
  P.observableIsConcrete

theorem ytr_gravity_elastic_observable_prediction_is_allowed
    (P : YtRGravityElasticObservablePrediction) :
    YtRGravityElasticAllowedObservable P.selectionGate.selectedLaw P.observable :=
  P.allowedObservable

end Chronos.Frontier
