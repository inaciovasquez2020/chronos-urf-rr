import Chronos.Frontier.YtRGravityElasticSchemaValidationRun

namespace Chronos
namespace Frontier

structure YtRGravityElasticPredictionVectorRealDataRun where
  schemaRun : YtRGravityElasticSchemaValidationRun
  modelVersionFrozen : Bool
  predictionCodeFrozen : Bool
  noOutcomeLeakage : Bool
  realDataPredictionVectorProduced : Bool
  runMetadataRecorded : Bool
deriving Repr, DecidableEq

def YtRGravityElasticPredictionVectorRealDataRun.completed
    (r : YtRGravityElasticPredictionVectorRealDataRun) : Prop :=
  r.schemaRun.completed ∧
  r.modelVersionFrozen = true ∧
  r.predictionCodeFrozen = true ∧
  r.noOutcomeLeakage = true ∧
  r.realDataPredictionVectorProduced = true ∧
  r.runMetadataRecorded = true

theorem ytr_gravity_elastic_prediction_vector_real_data_run_closed
    (r : YtRGravityElasticPredictionVectorRealDataRun)
    (h_schema : r.schemaRun.completed)
    (h_model : r.modelVersionFrozen = true)
    (h_code : r.predictionCodeFrozen = true)
    (h_no_leak : r.noOutcomeLeakage = true)
    (h_vector : r.realDataPredictionVectorProduced = true)
    (h_metadata : r.runMetadataRecorded = true) :
    r.completed := by
  simp [
    YtRGravityElasticPredictionVectorRealDataRun.completed,
    h_schema,
    h_model,
    h_code,
    h_no_leak,
    h_vector,
    h_metadata
  ]

end Frontier
end Chronos
