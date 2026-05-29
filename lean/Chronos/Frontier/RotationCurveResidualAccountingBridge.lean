import Chronos.Frontier.ObservedRotationCurveBudgetGateBridge

namespace Chronos.Frontier

/--
`RotationCurveResidualAccountingBridge` packages the finite observed
rotation-curve residual budget as an accounting residual.

This is a finite residual-accounting bridge only.
-/
structure RotationCurveResidualAccountingBridge where
  budgetGateBridge : ObservedRotationCurveBudgetGateBridge
  residualAccountedMass : Nat
  residualMatchesGateBudget :
    residualAccountedMass = budgetGateBridge.gateBudget

def RotationCurveResidualAccountingBridge.residual
    (B : RotationCurveResidualAccountingBridge) : Nat :=
  B.residualAccountedMass

theorem RotationCurveResidualAccountingBridge.residual_matches_gate
    (B : RotationCurveResidualAccountingBridge) :
    B.residualAccountedMass = B.budgetGateBridge.gateBudget :=
  B.residualMatchesGateBudget

theorem RotationCurveResidualAccountingBridge.residual_matches_observed_budget_residual
    (B : RotationCurveResidualAccountingBridge) :
    B.residualAccountedMass =
      B.budgetGateBridge.rotationBudget.residualBudget := by
  rw [B.residualMatchesGateBudget, B.budgetGateBridge.gateMatchesResidual]

/--
A finite actual-value residual accounting witness.

Required finite accounting tokens:
observedBudget = 100
baryonicAccountedBudget = 72
residualAccountedMass = 28
100 = 72 + 28
-/
def rotationCurveResidualAccountingWitnessBudget : ObservedRotationCurveBudget where
  observedBudget := 100
  baryonicAccountedBudget := 72
  residualBudget := 28
  budgetClosed := by native_decide

theorem rotation_curve_residual_accounting_actual_values :
    rotationCurveResidualAccountingWitnessBudget.observedBudget = 100 ∧
    rotationCurveResidualAccountingWitnessBudget.baryonicAccountedBudget = 72 ∧
    rotationCurveResidualAccountingWitnessBudget.residualBudget = 28 :=
  by native_decide

theorem rotation_curve_residual_accounting_closed :
    rotationCurveResidualAccountingWitnessBudget.observedBudget =
      rotationCurveResidualAccountingWitnessBudget.baryonicAccountedBudget +
        rotationCurveResidualAccountingWitnessBudget.residualBudget :=
  by native_decide

end Chronos.Frontier
