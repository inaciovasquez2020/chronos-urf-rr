import Chronos.Frontier.YtRGravityElasticBaselineComparisonRun

namespace Chronos
namespace Frontier

structure YtRGravityElasticHeldoutEvidenceCertificate where
  baselineRun : YtRGravityElasticBaselineComparisonRun
  holdoutSplitFrozen : Bool
  heldoutEvaluationExecuted : Bool
  uncertaintyAccountingExecuted : Bool
  acceptanceCriterionDeclared : Bool
  replicationPacketRecorded : Bool
  evidenceBoundaryPreserved : Bool
deriving Repr, DecidableEq

def YtRGravityElasticHeldoutEvidenceCertificate.completed
    (c : YtRGravityElasticHeldoutEvidenceCertificate) : Prop :=
  c.baselineRun.completed ∧
  c.holdoutSplitFrozen = true ∧
  c.heldoutEvaluationExecuted = true ∧
  c.uncertaintyAccountingExecuted = true ∧
  c.acceptanceCriterionDeclared = true ∧
  c.replicationPacketRecorded = true ∧
  c.evidenceBoundaryPreserved = true

theorem ytr_gravity_elastic_heldout_evidence_certificate_closed
    (c : YtRGravityElasticHeldoutEvidenceCertificate)
    (h_baseline : c.baselineRun.completed)
    (h_split : c.holdoutSplitFrozen = true)
    (h_eval : c.heldoutEvaluationExecuted = true)
    (h_uncertainty : c.uncertaintyAccountingExecuted = true)
    (h_acceptance : c.acceptanceCriterionDeclared = true)
    (h_replication : c.replicationPacketRecorded = true)
    (h_boundary : c.evidenceBoundaryPreserved = true) :
    c.completed := by
  simp [
    YtRGravityElasticHeldoutEvidenceCertificate.completed,
    h_baseline,
    h_split,
    h_eval,
    h_uncertainty,
    h_acceptance,
    h_replication,
    h_boundary
  ]

end Frontier
end Chronos
