import Chronos.Frontier.RotationCurveAuthenticPayloadTarget

namespace Chronos.Frontier

structure BoundedSyntheticRotationCurvePayloadGate where
  authenticPayloadTargetClosed : Bool
  boundedSyntheticPayloadDeclared : Bool
  finiteRadiusVectorDeclared : Bool
  finiteVelocityVectorDeclared : Bool
  finiteUncertaintyVectorDeclared : Bool
  schemaTestOnly : Bool
  authenticPayloadBound : Bool
  empiricalRunClosed : Bool
  empiricalFitClaim : Bool
  galaxyDataIngestionClaim : Bool
  darkMatterReplacementClaim : Bool
  lambdaCDMFailureClaim : Bool
deriving Repr, DecidableEq

def boundedSyntheticRotationCurvePayloadGate :
    BoundedSyntheticRotationCurvePayloadGate :=
  {
    authenticPayloadTargetClosed := true
    boundedSyntheticPayloadDeclared := true
    finiteRadiusVectorDeclared := true
    finiteVelocityVectorDeclared := true
    finiteUncertaintyVectorDeclared := true
    schemaTestOnly := true
    authenticPayloadBound := false
    empiricalRunClosed := false
    empiricalFitClaim := false
    galaxyDataIngestionClaim := false
    darkMatterReplacementClaim := false
    lambdaCDMFailureClaim := false
  }

theorem boundedSyntheticRotationCurvePayloadGate_guard :
    boundedSyntheticRotationCurvePayloadGate.authenticPayloadTargetClosed = true ∧
    boundedSyntheticRotationCurvePayloadGate.boundedSyntheticPayloadDeclared = true ∧
    boundedSyntheticRotationCurvePayloadGate.finiteRadiusVectorDeclared = true ∧
    boundedSyntheticRotationCurvePayloadGate.finiteVelocityVectorDeclared = true ∧
    boundedSyntheticRotationCurvePayloadGate.finiteUncertaintyVectorDeclared = true ∧
    boundedSyntheticRotationCurvePayloadGate.schemaTestOnly = true ∧
    boundedSyntheticRotationCurvePayloadGate.authenticPayloadBound = false ∧
    boundedSyntheticRotationCurvePayloadGate.empiricalRunClosed = false ∧
    boundedSyntheticRotationCurvePayloadGate.empiricalFitClaim = false ∧
    boundedSyntheticRotationCurvePayloadGate.galaxyDataIngestionClaim = false ∧
    boundedSyntheticRotationCurvePayloadGate.darkMatterReplacementClaim = false ∧
    boundedSyntheticRotationCurvePayloadGate.lambdaCDMFailureClaim = false := by
  native_decide

end Chronos.Frontier
