import Chronos.Frontier.RestrictedContinuationNormControlAnalyticPDEEstimatePayload

structure RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionHypotheses where
  inputSurface : RestrictedContinuationNormControlAnalyticEstimateInputSurfaceHypotheses
  bridgePayloadConstruction : inputSurface.estimateProofBridgeAvailable
  derivativeIdentityPayloadConstruction : inputSurface.data.derivativeIdentityInput
  fluxNonnegativityPayloadConstruction : inputSurface.data.fluxNonnegativityInput
  bootstrapBoundsPayloadConstruction : inputSurface.data.bootstrapBoundsInput

def RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionPayload
    (h : RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionHypotheses) :
    RestrictedContinuationNormControlAnalyticPDEEstimatePayload :=
  { inputSurface := h.inputSurface
    bridgePayload := h.bridgePayloadConstruction
    derivativeIdentityPayload := h.derivativeIdentityPayloadConstruction
    fluxNonnegativityPayload := h.fluxNonnegativityPayloadConstruction
    bootstrapBoundsPayload := h.bootstrapBoundsPayloadConstruction }

def RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionClosed
    (h : RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionHypotheses) : Prop :=
  RestrictedContinuationNormControlAnalyticPDEEstimatePayloadClosed
    (RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionPayload h)

theorem RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstruction
    (h : RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionHypotheses) :
    RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionClosed h := by
  exact RestrictedContinuationNormControlAnalyticPDEEstimatePayloadClosure
    (RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionPayload h)

theorem RestrictedContinuationNormControlAnalyticEstimateFromConstructedAnalyticPDEEstimatePayload
    (h : RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionHypotheses) :
    RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputsClosed
      (RestrictedContinuationNormControlPDEInputPackageConstructionPackage
        (RestrictedContinuationNormControlPDEComponentInputConstructionsPackageHypotheses
          (RestrictedContinuationNormControlComponentAnalyticEstimatesComponentInputHypotheses
            (RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofsComponentHypotheses
              (RestrictedContinuationNormControlAnalyticPDEEstimatePayloadProofHypotheses
                (RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionPayload h)))))) := by
  exact RestrictedContinuationNormControlAnalyticEstimateFromAnalyticPDEEstimatePayload
    (RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionPayload h)

def RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionStatus : String :=
  "CONDITIONAL_ANALYTIC_PDE_ESTIMATE_PAYLOAD_CONSTRUCTION"

def RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionPreviousObject : String :=
  "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD"

def RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionRemainingObject : String :=
  "RESTRICTED_CONTINUATION_NORM_CONTROL_PAYLOAD_FIELD_ANALYTIC_PROOFS"
