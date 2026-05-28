#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
lean = root / "lean/Chronos/Frontier/ObservedRotationCurveBudgetGateBridge.lean"
art = root / "artifacts/chronos/observed_rotation_curve_budget_gate_bridge_2026_05_28.json"
doc = root / "docs/status/OBSERVED_ROTATION_CURVE_BUDGET_GATE_BRIDGE_2026_05_28.md"

for p in (lean, art, doc):
    if not p.exists():
        raise SystemExit(f"missing required file: {p}")

lean_text = lean.read_text()
required_tokens = [
    "structure PhysicalDetectorFieldWithDynamics",
    "def requiredMassFromRotation",
    "def physicalGDMBudget",
    "physicalGDMBudget_partitioned_certificate_from_observed_rotation_curve",
    "theorem physicalGDM_observed_rotation_curve_feeds_gate",
    "PartitionedPhysicalDetectorBudgetCertificate",
    "RestrictedFiniteDetectorGate",
    "partitionedBudgetCertificate_feeds_restrictedFiniteDetectorGate_derived",
]
for token in required_tokens:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

data = json.loads(art.read_text())
if data.get("status") != "CONDITIONAL_OBSERVED_RESIDUAL_TO_RESTRICTED_GATE_BRIDGE":
    raise SystemExit("bad artifact status")

doc_text = doc.read_text()
boundary_tokens = [
    "Does not prove",
    "galaxy rotation curve fit",
    "lensing fit",
    "empirical dark-matter replacement",
    "Lambda-CDM refutation",
    "Chronos-RR",
    "P vs NP",
    "Clay problem",
]
for token in boundary_tokens:
    if token not in doc_text:
        raise SystemExit(f"missing boundary token: {token}")

print("OBSERVED_ROTATION_CURVE_BUDGET_GATE_BRIDGE_OK")
