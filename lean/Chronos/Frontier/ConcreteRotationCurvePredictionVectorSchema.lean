import Chronos.Frontier.RotationCurveDeficitMassModelComparisonInterface

namespace Chronos.Frontier

structure ConcreteRotationCurvePredictionVectorSchema where
  modelComparisonInterfaceClosed : Bool
  radiusSlotDeclared : Bool
  observedVelocitySlotDeclared : Bool
  baryonicVelocitySlotDeclared : Bool
  deficitMassPredictionSlotDeclared : Bool
  uncertaintySlotDeclared : Bool
  empiricalFitClaim : Bool
  galaxyDataIngestionClaim : Bool
deriving Repr, DecidableEq

def concreteRotationCurvePredictionVectorSchema :
    ConcreteRotationCurvePredictionVectorSchema :=
  {
    modelComparisonInterfaceClosed := true
    radiusSlotDeclared := true
    observedVelocitySlotDeclared := true
    baryonicVelocitySlotDeclared := true
    deficitMassPredictionSlotDeclared := true
    uncertaintySlotDeclared := true
    empiricalFitClaim := false
    galaxyDataIngestionClaim := false
  }

theorem concreteRotationCurvePredictionVectorSchema_guard :
    concreteRotationCurvePredictionVectorSchema.modelComparisonInterfaceClosed = true ∧
    concreteRotationCurvePredictionVectorSchema.radiusSlotDeclared = true ∧
    concreteRotationCurvePredictionVectorSchema.observedVelocitySlotDeclared = true ∧
    concreteRotationCurvePredictionVectorSchema.baryonicVelocitySlotDeclared = true ∧
    concreteRotationCurvePredictionVectorSchema.deficitMassPredictionSlotDeclared = true ∧
    concreteRotationCurvePredictionVectorSchema.uncertaintySlotDeclared = true ∧
    concreteRotationCurvePredictionVectorSchema.empiricalFitClaim = false ∧
    concreteRotationCurvePredictionVectorSchema.galaxyDataIngestionClaim = false := by
  native_decide

end Chronos.Frontier
