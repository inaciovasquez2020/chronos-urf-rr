import Chronos.Frontier.RestrictedContinuationNormControlAnalyticEstimateInputSurface

structure RestrictedContinuationNormControlAnalyticEstimateProofHypotheses where
  inputSurface : RestrictedContinuationNormControlAnalyticEstimateInputSurfaceHypotheses
  estimateProofBridgeAvailable : Prop
  derivativeIdentityAvailable : inputSurface.data.derivativeIdentityInput
  fluxNonnegativityAvailable : inputSurface.data.fluxNonnegativityInput
  bootstrapBoundsAvailable : inputSurface.data.bootstrapBoundsInput

def RestrictedContinuationNormControlAnalyticEstimateProofClosed
    (h : RestrictedContinuationNormControlAnalyticEstimateProofHypotheses) : Prop :=
  h.inputSurface.data.analyticEstimateInput

theorem RestrictedContinuationNormControlAnalyticEstimateProof
    (h : RestrictedContinuationNormControlAnalyticEstimateProofHypotheses)
    (h_bridge : h.inputSurface.estimateProofBridgeAvailable) :
    RestrictedContinuationNormControlAnalyticEstimateProofClosed h := by
  have h_obligation :
      RestrictedContinuationNormControlAnalyticEstimateInputObligation h.inputSurface.data :=
    RestrictedContinuationNormControlAnalyticEstimateInputSurface h.inputSurface h_bridge
  exact h_obligation
    h.derivativeIdentityAvailable
    h.fluxNonnegativityAvailable
    h.bootstrapBoundsAvailable

def RestrictedContinuationNormControlAnalyticEstimateProofStatus : String :=
  "CONDITIONAL_PROOF_OBJECT_ANALYTIC_ESTIMATE_INPUT_REQUIRED"

def RestrictedContinuationNormControlAnalyticEstimateProofPreviousObject : String :=
  "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_INPUT_SURFACE"

def RestrictedContinuationNormControlAnalyticEstimateProofRemainingObject : String :=
  "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_DERIVATION_FROM_PDE_INPUTS"
