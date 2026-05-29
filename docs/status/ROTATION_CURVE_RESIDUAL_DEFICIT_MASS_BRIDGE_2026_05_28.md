# ROTATION_CURVE_RESIDUAL_DEFICIT_MASS_BRIDGE_2026_05_28

Status: `FINITE_DEFICIT_MASS_ACCOUNTING_BRIDGE_ONLY`

Object: `RotationCurveResidualDeficitMassBridge`

This status surface adds a finite bridge from rotation-curve residual accounting to deficit-mass accounting.

Closed dependency:

```text
RotationCurveResidualAccountingBridge
  → RotationCurveResidualDeficitMassBridge
The Lean module introduces:
RotationCurveResidualDeficitMassBridge,
RotationCurveResidualDeficitMassBridge.deficit,
RotationCurveResidualDeficitMassBridge.residual_matches_deficit,
RotationCurveResidualDeficitMassBridge.deficit_matches_gate_budget,
RotationCurveResidualDeficitMassBridge.deficit_matches_observed_residual,
rotationCurveResidualDeficitMassWitnessBudget,
rotation_curve_residual_deficit_mass_actual_values,
rotation_curve_residual_deficit_mass_closed.
Actual finite witness:
observedBudget = 100
baryonicAccountedBudget = 72
residualAccountedMass = 28
geometricDeficitMass = 28
100 = 72 + 28
Boundary
This is a finite deficit-mass accounting bridge only.
Does not prove:
empirical rotation-curve fit,
galaxy data ingestion,
dark matter replacement,
Lambda-CDM failure,
modified gravity claim,
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
