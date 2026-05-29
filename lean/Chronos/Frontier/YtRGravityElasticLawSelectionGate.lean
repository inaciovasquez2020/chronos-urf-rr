namespace Chronos.Frontier

inductive YtRGravityElasticCandidateLaw where
  | scalarDeformation
  | potentialWall
  | curvatureStrain
  | metricElastic
  | tidalRestoring
deriving DecidableEq, Repr

def YtRGravityElasticCandidateLaw.isSerious : YtRGravityElasticCandidateLaw → Bool
  | .metricElastic => true
  | .tidalRestoring => true
  | _ => false

structure YtRGravityElasticLawSelectionGate where
  selectedLaw : YtRGravityElasticCandidateLaw
  selectedLawIsSerious : selectedLaw.isSerious = true
  boundary :
    selectedLaw = YtRGravityElasticCandidateLaw.metricElastic ∨
    selectedLaw = YtRGravityElasticCandidateLaw.tidalRestoring

def YtRMetricElasticLawSelectionGate : YtRGravityElasticLawSelectionGate where
  selectedLaw := YtRGravityElasticCandidateLaw.metricElastic
  selectedLawIsSerious := rfl
  boundary := Or.inl rfl

def YtRTidalRestoringLawSelectionGate : YtRGravityElasticLawSelectionGate where
  selectedLaw := YtRGravityElasticCandidateLaw.tidalRestoring
  selectedLawIsSerious := rfl
  boundary := Or.inr rfl

theorem selected_ytr_gravity_elastic_law_is_serious
  (G : YtRGravityElasticLawSelectionGate) :
  G.selectedLaw.isSerious = true :=
  G.selectedLawIsSerious

theorem selected_ytr_gravity_elastic_law_is_metric_or_tidal
  (G : YtRGravityElasticLawSelectionGate) :
  G.selectedLaw = YtRGravityElasticCandidateLaw.metricElastic ∨
  G.selectedLaw = YtRGravityElasticCandidateLaw.tidalRestoring :=
  G.boundary

end Chronos.Frontier
