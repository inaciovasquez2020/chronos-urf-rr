import Chronos.Frontier.YtRGravityElasticPredictionVectorRealDataRun

namespace Chronos
namespace Frontier

structure YtRGravityElasticBaselineComparisonRun where
  predictionRun : YtRGravityElasticPredictionVectorRealDataRun
  standardGRComparisonExecuted : Bool
  lambdaCDMComparisonExecuted : Bool
  commonMetricDeclared : Bool
  baselineMetricsRecorded : Bool
  comparisonResultFrozen : Bool
  uncertaintyInputsRecorded : Bool
deriving Repr, DecidableEq

def YtRGravityElasticBaselineComparisonRun.completed
    (r : YtRGravityElasticBaselineComparisonRun) : Prop :=
  r.predictionRun.completed ∧
  r.standardGRComparisonExecuted = true ∧
  r.lambdaCDMComparisonExecuted = true ∧
  r.commonMetricDeclared = true ∧
  r.baselineMetricsRecorded = true ∧
  r.comparisonResultFrozen = true ∧
  r.uncertaintyInputsRecorded = true

theorem ytr_gravity_elastic_baseline_comparison_run_closed
    (r : YtRGravityElasticBaselineComparisonRun)
    (h_prediction : r.predictionRun.completed)
    (h_gr : r.standardGRComparisonExecuted = true)
    (h_lcdm : r.lambdaCDMComparisonExecuted = true)
    (h_metric : r.commonMetricDeclared = true)
    (h_baseline : r.baselineMetricsRecorded = true)
    (h_result : r.comparisonResultFrozen = true)
    (h_uncertainty : r.uncertaintyInputsRecorded = true) :
    r.completed := by
  simp [
    YtRGravityElasticBaselineComparisonRun.completed,
    h_prediction,
    h_gr,
    h_lcdm,
    h_metric,
    h_baseline,
    h_result,
    h_uncertainty
  ]

end Frontier
end Chronos
