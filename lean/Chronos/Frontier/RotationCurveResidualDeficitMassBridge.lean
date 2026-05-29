import Chronos.Frontier.RotationCurveResidualAccountingBridge

namespace Chronos.Frontier

/--
`RotationCurveResidualDeficitMassBridge` repackages a finite rotation-curve
residual accounting mass as a finite deficit-mass accounting object.

This is only a finite accounting bridge. It does not assert empirical galaxy
data, dark matter replacement, modified gravity, or PDE/gravity closure.
-/
structure RotationCurveResidualDeficitMassBridge where
  residualAccounting : RotationCurveResidualAccountingBridge
  geometricDeficitMass : Nat
  residualEqualsDeficit :
    residualAccounting.residualAccountedMass = geometricDeficitMass

def RotationCurveResidualDeficitMassBridge.deficit
    (B : RotationCurveResidualDeficitMassBridge) : Nat :=
  B.geometricDeficitMass

theorem RotationCurveResidualDeficitMassBridge.residual_matches_deficit
    (B : RotationCurveResidualDeficitMassBridge) :
    B.residualAccounting.residualAccountedMass = B.geometricDeficitMass :=
  B.residualEqualsDeficit

theorem RotationCurveResidualDeficitMassBridge.deficit_matches_gate_budget
    (B : RotationCurveResidualDeficitMassBridge) :
    B.geometricDeficitMass =
      B.residualAccounting.budgetGateBridge.gateBudget := by
  rw [← B.residualEqualsDeficit]
  exact B.residualAccounting.residualMatchesGateBudget

theorem RotationCurveResidualDeficitMassBridge.deficit_matches_observed_residual
    (B : RotationCurveResidualDeficitMassBridge) :
    B.geometricDeficitMass =
      B.residualAccounting.budgetGateBridge.rotationBudget.residualBudget := by
  rw [← B.residualEqualsDeficit]
  exact B.residualAccounting.residual_matches_observed_budget_residual

/--
Finite actual-value deficit-mass witness.

Required finite accounting tokens:
observedBudget = 100
baryonicAccountedBudget = 72
residualAccountedMass = 28
geometricDeficitMass = 28
100 = 72 + 28
-/
def rotationCurveResidualDeficitMassWitnessBudget : ObservedRotationCurveBudget where
  observedBudget := 100
  baryonicAccountedBudget := 72
  residualBudget := 28
  budgetClosed := by native_decide

theorem rotation_curve_residual_deficit_mass_actual_values :
    rotationCurveResidualDeficitMassWitnessBudget.observedBudget = 100 ∧
    rotationCurveResidualDeficitMassWitnessBudget.baryonicAccountedBudget = 72 ∧
    rotationCurveResidualDeficitMassWitnessBudget.residualBudget = 28 :=
  by native_decide

theorem rotation_curve_residual_deficit_mass_closed :
    rotationCurveResidualDeficitMassWitnessBudget.observedBudget =
      rotationCurveResidualDeficitMassWitnessBudget.baryonicAccountedBudget +
        rotationCurveResidualDeficitMassWitnessBudget.residualBudget :=
  by native_decide

end Chronos.Frontier
