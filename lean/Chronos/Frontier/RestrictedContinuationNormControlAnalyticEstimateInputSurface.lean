import Chronos.Frontier.RestrictedContinuationNormControlEstimateProofBridge

structure RestrictedContinuationNormControlAnalyticEstimateInputData where
  proofBridgeData : RestrictedContinuationNormControlEstimateProofBridgeData
  derivativeIdentityInput : Prop
  fluxNonnegativityInput : Prop
  bootstrapBoundsInput : Prop
  analyticEstimateInput : Prop

def RestrictedContinuationNormControlAnalyticEstimateInputObligation
    (D : RestrictedContinuationNormControlAnalyticEstimateInputData) : Prop :=
  D.derivativeIdentityInput →
  D.fluxNonnegativityInput →
  D.bootstrapBoundsInput →
  D.analyticEstimateInput

structure RestrictedContinuationNormControlAnalyticEstimateInputSurfaceHypotheses where
  data : RestrictedContinuationNormControlAnalyticEstimateInputData
  estimateProofBridgeAvailable : Prop
  analyticEstimateInputStated :
    RestrictedContinuationNormControlAnalyticEstimateInputObligation data

def RestrictedContinuationNormControlAnalyticEstimateInputSurfaceClosed
    (h : RestrictedContinuationNormControlAnalyticEstimateInputSurfaceHypotheses) : Prop :=
  h.estimateProofBridgeAvailable →
  RestrictedContinuationNormControlAnalyticEstimateInputObligation h.data

theorem RestrictedContinuationNormControlAnalyticEstimateInputSurface
    (h : RestrictedContinuationNormControlAnalyticEstimateInputSurfaceHypotheses) :
    RestrictedContinuationNormControlAnalyticEstimateInputSurfaceClosed h := by
  intro _
  exact h.analyticEstimateInputStated
