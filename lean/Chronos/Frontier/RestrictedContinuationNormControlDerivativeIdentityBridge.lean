import Chronos.Frontier.DerivativeIdentityObligationSurface
import Chronos.Frontier.RestrictedContinuationNormControlProof

structure RestrictedContinuationNormControlDerivativeIdentityBridgeData where
  derivativeIdentityData : DerivativeIdentityObligationData
  continuationNormControlTarget : Prop

def RestrictedContinuationNormControlDerivativeIdentityBridgeObligation
    (D : RestrictedContinuationNormControlDerivativeIdentityBridgeData) : Prop :=
  DerivativeIdentityObligation D.derivativeIdentityData →
  D.continuationNormControlTarget

structure RestrictedContinuationNormControlDerivativeIdentityBridgeHypotheses where
  data : RestrictedContinuationNormControlDerivativeIdentityBridgeData
  derivativeIdentityObligationSurfaceAvailable : Prop
  restrictedContinuationNormControlProofSurfaceAvailable : Prop
  bridgeObligationStated :
    RestrictedContinuationNormControlDerivativeIdentityBridgeObligation data

def RestrictedContinuationNormControlDerivativeIdentityBridgeClosed
    (h : RestrictedContinuationNormControlDerivativeIdentityBridgeHypotheses) : Prop :=
  h.derivativeIdentityObligationSurfaceAvailable →
  h.restrictedContinuationNormControlProofSurfaceAvailable →
  RestrictedContinuationNormControlDerivativeIdentityBridgeObligation h.data

theorem RestrictedContinuationNormControlDerivativeIdentityBridge
    (h : RestrictedContinuationNormControlDerivativeIdentityBridgeHypotheses) :
    RestrictedContinuationNormControlDerivativeIdentityBridgeClosed h := by
  intro _ _
  exact h.bridgeObligationStated
