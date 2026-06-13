import Chronos.Frontier.RestrictedContinuationNormControlEstimateObligationSurface
import Chronos.Frontier.RestrictedContinuationNormControlProof

structure RestrictedContinuationNormControlEstimateProofBridgeData where
  estimateData : RestrictedContinuationNormControlEstimateData
  restrictedContinuationNormControlProofSurface : Prop

def RestrictedContinuationNormControlEstimateProofBridgeObligation
    (D : RestrictedContinuationNormControlEstimateProofBridgeData) : Prop :=
  RestrictedContinuationNormControlEstimateObligation D.estimateData →
  D.restrictedContinuationNormControlProofSurface

structure RestrictedContinuationNormControlEstimateProofBridgeHypotheses where
  data : RestrictedContinuationNormControlEstimateProofBridgeData
  estimateObligationSurfaceAvailable : Prop
  restrictedContinuationNormControlProofAvailable : Prop
  proofBridgeStated :
    RestrictedContinuationNormControlEstimateProofBridgeObligation data

def RestrictedContinuationNormControlEstimateProofBridgeClosed
    (h : RestrictedContinuationNormControlEstimateProofBridgeHypotheses) : Prop :=
  h.estimateObligationSurfaceAvailable →
  h.restrictedContinuationNormControlProofAvailable →
  RestrictedContinuationNormControlEstimateProofBridgeObligation h.data

theorem RestrictedContinuationNormControlEstimateProofBridge
    (h : RestrictedContinuationNormControlEstimateProofBridgeHypotheses) :
    RestrictedContinuationNormControlEstimateProofBridgeClosed h := by
  intro _ _
  exact h.proofBridgeStated
