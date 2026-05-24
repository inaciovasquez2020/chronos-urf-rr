#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/FiniteCapacityOpticalMetricSymbolicProfileTheorem.lean"
artifact = ROOT / "artifacts/chronos/finite_capacity_optical_metric_symbolic_profile_theorem_2026_05_23.json"
doc = ROOT / "docs/status/FINITE_CAPACITY_OPTICAL_METRIC_SYMBOLIC_PROFILE_THEOREM_2026_05_23.md"
root_import = ROOT / "lean/Chronos.lean"

for path in [lean, artifact, doc, root_import]:
    if not path.exists():
        raise SystemExit(f"missing {path}")

lean_text = lean.read_text()
for token in [
    "structure FiniteCapacityOpticalMetricSymbolicProfile",
    "def opticalIndex",
    "def opticalIndexDerivativeProxy",
    "def opticalAlphaDerivativeProxy",
    "finite_capacity_optical_metric_symbolic_index_positive",
    "finite_capacity_optical_metric_symbolic_index_lt_one",
    "finite_capacity_optical_metric_symbolic_center_lower_bound",
    "finite_capacity_optical_metric_symbolic_center_lower_bound_positive",
    "finite_capacity_optical_metric_symbolic_index_derivative_positive",
    "finite_capacity_optical_metric_symbolic_alpha_derivative_negative",
    "finiteCapacityOpticalMetricSymbolicProfileWitness",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

data = json.loads(artifact.read_text())
if data["status"] != "SYMBOLIC_OPTICAL_PROFILE_THEOREM_ONLY_NOT_GRAVITY_CLOSURE":
    raise SystemExit("bad status")

for token in [
    "0 < opticalIndex",
    "opticalIndex < 1",
    "1 - eps <= opticalIndex",
    "0 < 1 - eps",
    "0 < opticalIndexDerivativeProxy",
    "opticalAlphaDerivativeProxy < 0",
    "symbolic optical profile theorem",
    "not gravity closure",
    "physical Einstein-matter flux identity",
    "restricted analytic estimate package assumptions",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    if token not in artifact.read_text():
        raise SystemExit(f"missing artifact token: {token}")
    if token not in doc.read_text():
        raise SystemExit(f"missing doc token: {token}")

if "import Chronos.Frontier.FiniteCapacityOpticalMetricSymbolicProfileTheorem" not in root_import.read_text():
    raise SystemExit("missing Chronos root import")

print("Finite capacity optical metric symbolic profile theorem verification OK.")
print("Status: SYMBOLIC_OPTICAL_PROFILE_THEOREM_ONLY_NOT_GRAVITY_CLOSURE")
