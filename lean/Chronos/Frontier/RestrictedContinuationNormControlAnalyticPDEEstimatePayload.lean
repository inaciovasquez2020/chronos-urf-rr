import Chronos.Frontier.RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofs

structure RestrictedContinuationNormControlAnalyticPDEEstimatePayload where
  inputSurface : RestrictedContinuationNormControlAnalyticEstimateInputSurfaceHypotheses
  bridgePayload : inputSurface.estimateProofBridgeAvailable
  derivativeIdentityPayload : inputSurface.data.derivativeIdentityInput
  fluxNonnegativityPayload : inputSurface.data.fluxNonnegativityInput
  bootstrapBoundsPayload : inputSurface.data.bootstrapBoundsInput

def RestrictedContinuationNormControlAnalyticPDEEstimatePayloadProofHypotheses
    (p : RestrictedContinuationNormControlAnalyticPDEEstimatePayload) :
    RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofsHypotheses :=
  { inputSurface := p.inputSurface
    bridgeAnalyticEstimateProof := p.bridgePayload
    derivativeIdentityAnalyticEstimateProof := p.derivativeIdentityPayload
    fluxNonnegativityAnalyticEstimateProof := p.fluxNonnegativityPayload
    bootstrapBoundsAnalyticEstimateProof := p.bootstrapBoundsPayload }

def RestrictedContinuationNormControlAnalyticPDEEstimatePayloadClosed
    (p : RestrictedContinuationNormControlAnalyticPDEEstimatePayload) : Prop :=
  RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofsClosed
    (RestrictedContinuationNormControlAnalyticPDEEstimatePayloadProofHypotheses p)

theorem RestrictedContinuationNormControlAnalyticPDEEstimatePayloadClosure
    (p : RestrictedContinuationNormControlAnalyticPDEEstimatePayload) :
    RestrictedContinuationNormControlAnalyticPDEEstimatePayloadClosed p := by
  exact RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofs
    (RestrictedContinuationNormControlAnalyticPDEEstimatePayloadProofHypotheses p)

theorem RestrictedContinuationNormControlAnalyticEstimateFromAnalyticPDEEstimatePayload
    (p : RestrictedContinuationNormControlAnalyticPDEEstimatePayload) :
    RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputsClosed
      (RestrictedContinuationNormControlPDEInputPackageConstructionPackage
        (RestrictedContinuationNormControlPDEComponentInputConstructionsPackageHypotheses
          (RestrictedContinuationNormControlComponentAnalyticEstimatesComponentInputHypotheses
            (RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofsComponentHypotheses
              (RestrictedContinuationNormControlAnalyticPDEEstimatePayloadProofHypotheses p))))) := by
  exact RestrictedContinuationNormControlAnalyticEstimateFromDerivativeFluxBootstrapProofs
    (RestrictedContinuationNormControlAnalyticPDEEstimatePayloadProofHypotheses p)

def RestrictedContinuationNormControlAnalyticPDEEstimatePayloadStatus : String :=
  "CONDITIONAL_ANALYTIC_PDE_ESTIMATE_PAYLOAD"

def RestrictedContinuationNormControlAnalyticPDEEstimatePayloadPreviousObject : String :=
  "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_FLUX_BOOTSTRAP_ANALYTIC_ESTIMATE_PROOFS"

def RestrictedContinuationNormControlAnalyticPDEEstimatePayloadRemainingObject : String :=
  "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD_CONSTRUCTION"
