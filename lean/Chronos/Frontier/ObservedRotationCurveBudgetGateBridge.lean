import Chronos.Frontier.PhysicalDetectorFieldExtractionMap

namespace Chronos.Frontier

/--
`ObservedRotationCurveBudget` is a finite arithmetic accounting object.

It records an observed velocity/mass-budget total, a baryonic-accounted
budget, and a residual budget, together with the finite equality certifying
that the observed budget decomposes into accounted plus residual budget.
-/
structure ObservedRotationCurveBudget where
  observedBudget : Nat
  baryonicAccountedBudget : Nat
  residualBudget : Nat
  budgetClosed : observedBudget = baryonicAccountedBudget + residualBudget

def ObservedRotationCurveBudget.residual
    (B : ObservedRotationCurveBudget) : Nat :=
  B.residualBudget

theorem ObservedRotationCurveBudget.closed
    (B : ObservedRotationCurveBudget) :
    B.observedBudget = B.baryonicAccountedBudget + B.residualBudget :=
  B.budgetClosed

/--
`ObservedRotationCurveBudgetGateBridge` attaches the already-closed finite
physical detector extraction map to an observed rotation-curve residual budget.

This is only a finite budget-to-gate interface bridge.
-/
structure ObservedRotationCurveBudgetGateBridge where
  detectorMap : PhysicalDetectorFieldExtractionMap
  rotationBudget : ObservedRotationCurveBudget
  detectorCompatible : detectorMap.detectorBudgetCompatible
  gateBudget : Nat
  gateMatchesResidual : gateBudget = rotationBudget.residualBudget

def ObservedRotationCurveBudgetGateBridge.restrictedGate
    (B : ObservedRotationCurveBudgetGateBridge) :
    B.detectorMap.restrictedFiniteDetectorExtractionGate :=
  B.detectorMap.compatibilityToGate B.detectorCompatible

theorem ObservedRotationCurveBudgetGateBridge.gate_budget_matches_residual
    (B : ObservedRotationCurveBudgetGateBridge) :
    B.gateBudget = B.rotationBudget.residualBudget :=
  B.gateMatchesResidual

theorem ObservedRotationCurveBudgetGateBridge.observed_budget_decomposes
    (B : ObservedRotationCurveBudgetGateBridge) :
    B.rotationBudget.observedBudget =
      B.rotationBudget.baryonicAccountedBudget + B.rotationBudget.residualBudget :=
  B.rotationBudget.budgetClosed

def observedRotationCurveBudgetWitness : ObservedRotationCurveBudget where
  observedBudget := 100
  baryonicAccountedBudget := 72
  residualBudget := 28
  budgetClosed := by native_decide

theorem observed_rotation_curve_budget_actual_values :
    observedRotationCurveBudgetWitness.observedBudget = 100 ∧
    observedRotationCurveBudgetWitness.baryonicAccountedBudget = 72 ∧
    observedRotationCurveBudgetWitness.residualBudget = 28 :=
  by native_decide

theorem observed_rotation_curve_budget_closed :
    observedRotationCurveBudgetWitness.observedBudget =
      observedRotationCurveBudgetWitness.baryonicAccountedBudget +
        observedRotationCurveBudgetWitness.residualBudget :=
  by native_decide

end Chronos.Frontier
