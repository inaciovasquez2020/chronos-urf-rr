import Chronos.Frontier.AnalyticDiniEstimateBindingLemma
import Mathlib

namespace Chronos.Frontier

inductive GenuineAnalyticDiniEstimateProofFrontierStatus where
  | stoppedAtRepositoryLocalEnvelope
  | requiresGenuineAnalyticDiniEstimateProof

def genuineAnalyticDiniEstimateProofFrontierStatus :
    GenuineAnalyticDiniEstimateProofFrontierStatus :=
  GenuineAnalyticDiniEstimateProofFrontierStatus.requiresGenuineAnalyticDiniEstimateProof

theorem genuineAnalyticDiniEstimateProofFrontierStatus_eq :
    genuineAnalyticDiniEstimateProofFrontierStatus =
      GenuineAnalyticDiniEstimateProofFrontierStatus.requiresGenuineAnalyticDiniEstimateProof := rfl

def GenuineAnalyticDiniEstimateProofMinimalMissingObject : String :=
  "GENUINE_ANALYTIC_DINI_ESTIMATE_PROOF"

def GenuineAnalyticDiniEstimateProofBoundary : List String :=
  [
    "REPOSITORY_LOCAL_ENVELOPE_ALREADY_CLOSED",
    "GENUINE_ANALYTIC_DINI_ESTIMATE_PROOF_NOT_SUPPLIED",
    "NO_CONVERGENCE_CLAIM",
    "NO_SUMMABILITY_CLAIM",
    "NO_FINAL_ANALYTIC_RESULT",
    "NO_P_VS_NP_CLAIM",
    "NO_CLAY_CLAIM"
  ]

end Chronos.Frontier
