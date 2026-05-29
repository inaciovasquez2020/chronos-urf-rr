import Chronos.Frontier.ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel

namespace Chronos.Frontier

structure ThetaResidualLowParameterInput where
  galaxyId : Nat
  observedVelocitySquared : Nat
  baryonicVelocitySquared : Nat
deriving Repr, DecidableEq

def thetaResidual (r : ThetaResidualLowParameterInput) : Nat :=
  r.observedVelocitySquared - r.baryonicVelocitySquared

structure ThetaResidualLowParameterPredictionRule where
  model : ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel
  thetaNumerator : Nat
  thetaDenominator : Nat
  thetaDenominatorPositive : 0 < thetaDenominator
  thetaStrictlyBelowOne : thetaNumerator < thetaDenominator
  frozenBeforeLikelihoodGuard : Bool
  lowParameterGuard : Bool
  noEmpiricalValidationClaim : Bool
  noPhysicalReplacementClaim : Bool

def thetaDeficitNumerator
    (R : ThetaResidualLowParameterPredictionRule)
    (r : ThetaResidualLowParameterInput) : Nat :=
  R.thetaNumerator * thetaResidual r

def thetaPredictionNumerator
    (R : ThetaResidualLowParameterPredictionRule)
    (r : ThetaResidualLowParameterInput) : Nat :=
  R.thetaDenominator * r.baryonicVelocitySquared + thetaDeficitNumerator R r

def thetaRuleV1 : ThetaResidualLowParameterPredictionRule :=
  { model := concretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModelV1
    thetaNumerator := 1
    thetaDenominator := 2
    thetaDenominatorPositive := by decide
    thetaStrictlyBelowOne := by decide
    frozenBeforeLikelihoodGuard := true
    lowParameterGuard := true
    noEmpiricalValidationClaim := false
    noPhysicalReplacementClaim := false }

theorem thetaRuleV1_projects_to_concrete_model :
    thetaRuleV1.model =
      concretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModelV1 := by
  rfl

theorem thetaRuleV1_theta_denominator_positive :
    0 < thetaRuleV1.thetaDenominator :=
  thetaRuleV1.thetaDenominatorPositive

theorem thetaRuleV1_theta_strictly_below_one :
    thetaRuleV1.thetaNumerator < thetaRuleV1.thetaDenominator :=
  thetaRuleV1.thetaStrictlyBelowOne

theorem thetaRuleV1_has_frozen_before_likelihood_guard :
    thetaRuleV1.frozenBeforeLikelihoodGuard = true := by
  rfl

theorem thetaRuleV1_has_low_parameter_guard :
    thetaRuleV1.lowParameterGuard = true := by
  rfl

theorem thetaRuleV1_has_no_empirical_validation_claim :
    thetaRuleV1.noEmpiricalValidationClaim = false := by
  rfl

theorem thetaRuleV1_has_no_physical_replacement_claim :
    thetaRuleV1.noPhysicalReplacementClaim = false := by
  rfl

theorem thetaResidual_zero_when_observed_le_baryonic
    {r : ThetaResidualLowParameterInput}
    (h : r.observedVelocitySquared ≤ r.baryonicVelocitySquared) :
    thetaResidual r = 0 := by
  unfold thetaResidual
  exact Nat.sub_eq_zero_of_le h

theorem thetaPredictionNumerator_at_zero_residual
    (R : ThetaResidualLowParameterPredictionRule)
    (r : ThetaResidualLowParameterInput)
    (h : thetaResidual r = 0) :
    thetaPredictionNumerator R r =
      R.thetaDenominator * r.baryonicVelocitySquared := by
  unfold thetaPredictionNumerator thetaDeficitNumerator
  rw [h, Nat.mul_zero, Nat.add_zero]

end Chronos.Frontier
