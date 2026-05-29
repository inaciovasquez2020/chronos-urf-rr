#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/RotationCurveResidualAccountingBridge.lean"
ART = ROOT / "artifacts/chronos/rotation_curve_residual_accounting_bridge_2026_05_28.json"
DOC = ROOT / "docs/status/ROTATION_CURVE_RESIDUAL_ACCOUNTING_BRIDGE_2026_05_28.md"
CHRONOS = ROOT / "lean/Chronos.lean"

for path in [LEAN, ART, DOC, CHRONOS]:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")

lean = LEAN.read_text()
doc = DOC.read_text()
chronos = CHRONOS.read_text()
artifact = json.loads(ART.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.ObservedRotationCurveBudgetGateBridge",
    "structure RotationCurveResidualAccountingBridge",
    "budgetGateBridge : ObservedRotationCurveBudgetGateBridge",
    "residualMatchesGateBudget",
    "residual_matches_gate",
    "residual_matches_observed_budget_residual",
    "rotationCurveResidualAccountingWitnessBudget",
    "rotation_curve_residual_accounting_actual_values",
    "rotation_curve_residual_accounting_closed",
]

for token in required_lean_tokens:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")

if "import Chronos.Frontier.RotationCurveResidualAccountingBridge" not in chronos:
    raise SystemExit("missing Chronos import")

if artifact.get("id") != "ROTATION_CURVE_RESIDUAL_ACCOUNTING_BRIDGE_2026_05_28":
    raise SystemExit("bad artifact id")

if artifact.get("status") != "FINITE_RESIDUAL_ACCOUNTING_BRIDGE_ONLY":
    raise SystemExit("bad artifact status")

if "OBSERVED_ROTATION_CURVE_BUDGET_GATE_BRIDGE_2026_05_28" not in artifact.get("depends_on", []):
    raise SystemExit("missing observed rotation-curve dependency")

expected_witness = {
    "observedBudget": 100,
    "baryonicAccountedBudget": 72,
    "residualAccountedMass": 28,
}

if artifact.get("actual_value_witness") != expected_witness:
    raise SystemExit("bad actual value witness")

required_doc_tokens = [
    "FINITE_RESIDUAL_ACCOUNTING_BRIDGE_ONLY",
    "RotationCurveResidualAccountingBridge",
    "ObservedRotationCurveBudgetGateBridge",
    "100 = 72 + 28",
    "finite residual-accounting bridge only",
    "empirical rotation-curve fit",
    "galaxy data ingestion",
    "dark matter replacement",
    "Lambda-CDM failure",
    "modified gravity claim",
    "empirical detector correctness",
    "Einstein-matter PDE well-posedness",
    "cosmic censorship",
    "hoop conjecture",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for token in required_doc_tokens:
    if token not in doc:
        raise SystemExit(f"missing doc token: {token}")

print("ROTATION_CURVE_RESIDUAL_ACCOUNTING_BRIDGE_OK")
