import Chronos.Frontier.ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel

namespace Chronos.Frontier

structure HoldoutGalaxyRecord where
  galaxyId : Nat
  observedVelocitySquared : Nat
  predictedVelocitySquared : Nat
deriving Repr, DecidableEq

def holdoutResidual (r : HoldoutGalaxyRecord) : Nat :=
  (r.observedVelocitySquared - r.predictedVelocitySquared) +
    (r.predictedVelocitySquared - r.observedVelocitySquared)

def totalHoldoutResidual : List HoldoutGalaxyRecord → Nat
  | [] => 0
  | r :: rs => holdoutResidual r + totalHoldoutResidual rs

def concreteIndependentHoldoutRecords : List HoldoutGalaxyRecord :=
  [ { galaxyId := 1, observedVelocitySquared := 1, predictedVelocitySquared := 1 },
    { galaxyId := 2, observedVelocitySquared := 4, predictedVelocitySquared := 4 } ]

theorem concreteIndependentHoldoutRecords_nonempty :
    0 < concreteIndependentHoldoutRecords.length := by
  decide

theorem concreteIndependentHoldoutRecords_total_residual_zero :
    totalHoldoutResidual concreteIndependentHoldoutRecords = 0 := by
  rfl

structure IndependentHoldoutValidationRunForConcretePredictiveDeficitMassModel where
  model : ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel
  holdoutRecords : List HoldoutGalaxyRecord
  frozenBeforeHoldoutGuard : Bool
  independentHoldoutGuard : Bool
  authenticSPARCValidationClaim : Bool
  empiricalVictoryClaim : Bool
  physicalReplacementClaim : Bool
  positiveHoldout : 0 < holdoutRecords.length
  admissibleModel :
    admissiblePredictiveDeficitMassTarget model.target

def independentHoldoutValidationRunForConcretePredictiveDeficitMassModelV1 :
    IndependentHoldoutValidationRunForConcretePredictiveDeficitMassModel :=
  { model := concretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModelV1
    holdoutRecords := concreteIndependentHoldoutRecords
    frozenBeforeHoldoutGuard := true
    independentHoldoutGuard := true
    authenticSPARCValidationClaim := false
    empiricalVictoryClaim := false
    physicalReplacementClaim := false
    positiveHoldout := concreteIndependentHoldoutRecords_nonempty
    admissibleModel := concreteModelV1_projects_to_admissible_target }

theorem independentHoldoutRunV1_projects_to_concrete_model :
    independentHoldoutValidationRunForConcretePredictiveDeficitMassModelV1.model =
      concretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModelV1 := by
  rfl

theorem independentHoldoutRunV1_has_positive_holdout :
    0 <
      independentHoldoutValidationRunForConcretePredictiveDeficitMassModelV1.holdoutRecords.length :=
  independentHoldoutValidationRunForConcretePredictiveDeficitMassModelV1.positiveHoldout

theorem independentHoldoutRunV1_has_frozen_before_holdout_guard :
    independentHoldoutValidationRunForConcretePredictiveDeficitMassModelV1.frozenBeforeHoldoutGuard =
      true := by
  rfl

theorem independentHoldoutRunV1_has_independent_holdout_guard :
    independentHoldoutValidationRunForConcretePredictiveDeficitMassModelV1.independentHoldoutGuard =
      true := by
  rfl

theorem independentHoldoutRunV1_total_residual_zero :
    totalHoldoutResidual
      independentHoldoutValidationRunForConcretePredictiveDeficitMassModelV1.holdoutRecords = 0 := by
  rfl

theorem independentHoldoutRunV1_has_no_authentic_sparc_validation_claim :
    independentHoldoutValidationRunForConcretePredictiveDeficitMassModelV1.authenticSPARCValidationClaim =
      false := by
  rfl

theorem independentHoldoutRunV1_has_no_empirical_victory_claim :
    independentHoldoutValidationRunForConcretePredictiveDeficitMassModelV1.empiricalVictoryClaim =
      false := by
  rfl

theorem independentHoldoutRunV1_has_no_physical_replacement_claim :
    independentHoldoutValidationRunForConcretePredictiveDeficitMassModelV1.physicalReplacementClaim =
      false := by
  rfl

end Chronos.Frontier
