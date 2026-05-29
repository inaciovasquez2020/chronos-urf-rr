# OBSERVED_ROTATION_CURVE_BUDGET_GATE_BRIDGE_2026_05_28

Status: `FINITE_BUDGET_GATE_BRIDGE_ONLY`

Object: `ObservedRotationCurveBudgetGateBridge`

This status surface adds a finite bridge from the closed physical detector extraction map to an observed rotation-curve residual budget gate.

Closed dependency:

```text
PhysicalDetectorFieldExtractionMap
  → ObservedRotationCurveBudgetGateBridge
The Lean module introduces:
ObservedRotationCurveBudget,
ObservedRotationCurveBudget.closed,
ObservedRotationCurveBudgetGateBridge,
ObservedRotationCurveBudgetGateBridge.restrictedGate,
ObservedRotationCurveBudgetGateBridge.gate_budget_matches_residual,
observedRotationCurveBudgetWitness,
observed_rotation_curve_budget_actual_values,
observed_rotation_curve_budget_closed.
Actual finite witness:
observedBudget = 100
baryonicAccountedBudget = 72
residualBudget = 28
100 = 72 + 28
Boundary
This is a finite budget-gate bridge only.
Does not prove:
empirical rotation-curve fit,
galaxy data ingestion,
dark matter replacement,
Lambda-CDM failure,
coverage/disjointness/geometric partition correctness,
empirical detector correctness,
Einstein-matter PDE well-posedness,
trapped-surface formation,
black-hole formation,
cosmic censorship,
hoop conjecture,
unrestricted QL_CollapseGate,
unrestricted UniversalBoundaryCompactness,
unrestricted Chronos-RR,
unrestricted H4.1/FGL,
P vs NP,
any Clay problem.
