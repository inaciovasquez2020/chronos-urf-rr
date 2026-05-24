#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/FiniteCapacityOpticalMetricNumericalWitness.lean"
artifact = ROOT / "artifacts/chronos/finite_capacity_optical_metric_numerical_witness_2026_05_23.json"
doc = ROOT / "docs/status/FINITE_CAPACITY_OPTICAL_METRIC_NUMERICAL_WITNESS_2026_05_23.md"
root_import = ROOT / "lean/Chronos.lean"

for path in [lean, artifact, doc, root_import]:
    if not path.exists():
        raise SystemExit(f"missing {path}")

lean_text = lean.read_text()
for token in [
    "structure FiniteCapacityOpticalMetricNumericalWitness",
    "centerIndex := 1 / 2",
    "outerIndex := 3 / 4",
    "centerAlpha := 4",
    "outerAlpha := 16 / 9",
    "finite_capacity_optical_metric_value_test_lower_index_at_center",
    "finite_capacity_optical_metric_value_test_alpha_decreases_outward",
    "finite_capacity_optical_metric_value_test_alpha_bounded",
    "sourceMapOnlyNotTheoremInput",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

data = json.loads(artifact.read_text())
if data["status"] != "NUMERICAL_SANITY_WITNESS_ONLY_NOT_THEOREM_INPUT":
    raise SystemExit("bad status")

for token in [
    "1/2",
    "3/4",
    "16/9",
    "centerIndex < outerIndex",
    "outerAlpha < centerAlpha",
    "centerAlpha <= 4",
    "outerAlpha <= 4",
    "not a theorem input",
    "gravity closure",
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

if "import Chronos.Frontier.FiniteCapacityOpticalMetricNumericalWitness" not in root_import.read_text():
    raise SystemExit("missing Chronos root import")

print("Finite capacity optical metric numerical witness verification OK.")
print("Status: NUMERICAL_SANITY_WITNESS_ONLY_NOT_THEOREM_INPUT")
