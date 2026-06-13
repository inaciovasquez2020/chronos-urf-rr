import Chronos.Frontier.RestrictedContinuationNormControlDerivativeIdentityBridge

structure RestrictedContinuationNormControlEstimateData where
  derivativeIdentityData : DerivativeIdentityObligationData
  bootstrapBoundsAvailable : Prop
  fluxNonnegativityAvailable : Prop
  continuationNormControlTarget : Prop

def RestrictedContinuationNormControlEstimateObligation
    (D : RestrictedContinuationNormControlEstimateData) : Prop :=
  DerivativeIdentityObligation D.derivativeIdentityData →
  D.fluxNonnegativityAvailable →
  D.bootstrapBoundsAvailable →
  D.continuationNormControlTarget

structure RestrictedContinuationNormControlEstimateObligationSurfaceHypotheses where
  data : RestrictedContinuationNormControlEstimateData
  derivativeIdentityBridgeAvailable : Prop
  continuationProofSurfaceAvailable : Prop
  estimateObligationStated :
    RestrictedContinuationNormControlEstimateObligation data

def RestrictedContinuationNormControlEstimateObligationSurfaceClosed
    (h : RestrictedContinuationNormControlEstimateObligationSurfaceHypotheses) : Prop :=
  h.derivativeIdentityBridgeAvailable →
  h.continuationProofSurfaceAvailable →
  RestrictedContinuationNormControlEstimateObligation h.data

theorem RestrictedContinuationNormControlEstimateObligationSurface
    (h : RestrictedContinuationNormControlEstimateObligationSurfaceHypotheses) :
    RestrictedContinuationNormControlEstimateObligationSurfaceClosed h := by
  intro _ _
  exact h.estimateObligationStated
