import Chronos.Frontier.RestrictedContinuationNormControlAnalyticEstimateProof

structure RestrictedContinuationNormControlPDEInputPackage where
  inputSurface : RestrictedContinuationNormControlAnalyticEstimateInputSurfaceHypotheses
  bridgeAvailable : inputSurface.estimateProofBridgeAvailable
  derivativeIdentityDerivedFromPDE : inputSurface.data.derivativeIdentityInput
  fluxNonnegativityDerivedFromPDE : inputSurface.data.fluxNonnegativityInput
  bootstrapBoundsDerivedFromPDE : inputSurface.data.bootstrapBoundsInput

def RestrictedContinuationNormControlPDEInputPackage.proofHypotheses
    (p : RestrictedContinuationNormControlPDEInputPackage) :
    RestrictedContinuationNormControlAnalyticEstimateProofHypotheses :=
  { inputSurface := p.inputSurface
    estimateProofBridgeAvailable := p.inputSurface.estimateProofBridgeAvailable
    derivativeIdentityAvailable := p.derivativeIdentityDerivedFromPDE
    fluxNonnegativityAvailable := p.fluxNonnegativityDerivedFromPDE
    bootstrapBoundsAvailable := p.bootstrapBoundsDerivedFromPDE }

def RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputsClosed
    (p : RestrictedContinuationNormControlPDEInputPackage) : Prop :=
  RestrictedContinuationNormControlAnalyticEstimateProofClosed p.proofHypotheses

theorem RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputs
    (p : RestrictedContinuationNormControlPDEInputPackage) :
    RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputsClosed p := by
  exact RestrictedContinuationNormControlAnalyticEstimateProof
    p.proofHypotheses
    p.bridgeAvailable

def RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputsStatus : String :=
  "CONDITIONAL_DERIVATION_FROM_PDE_INPUT_PACKAGE"

def RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputsPreviousObject : String :=
  "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_PROOF"

def RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputsRemainingObject : String :=
  "RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_INPUT_PACKAGE_CONSTRUCTION"
