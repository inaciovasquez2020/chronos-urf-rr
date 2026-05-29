#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/SpacetimeFabricMetricInput.lean"
ART = ROOT / "artifacts/chronos/spacetime_fabric_metric_input_2026_05_29.json"
DOC = ROOT / "docs/status/SPACETIME_FABRIC_METRIC_INPUT_2026_05_29.md"
CHRONOS = ROOT / "lean/Chronos.lean"

lean_text = LEAN.read_text()
art_text = ART.read_text()
doc_text = DOC.read_text()
chronos_text = CHRONOS.read_text()
data = json.loads(art_text)

assert data["id"] == "SPACETIME_FABRIC_METRIC_INPUT_2026_05_29"
assert data["object"] == "SpacetimeFabricMetricInput"
assert data["status"] == "METRIC_CONTAINER_INPUT_ONLY_NO_NEW_GRAVITY_CLAIM"

required = [
    "smoothManifold4D",
    "lorentzianMetric",
    "metricSignatureRecorded",
    "leviCivitaConnectionRecorded",
    "riemannCurvatureTensorRecorded",
    "ricciCurvatureTensorRecorded",
    "scalarCurvatureRecorded",
    "stressEnergyTensorRecorded",
    "einsteinEquationReferenceRecorded",
    "ytrElasticResponseSlotRecorded",
    "boundaryPreserved",
]

for token in required:
    assert token in lean_text
    assert token in art_text
    assert token in doc_text

for token in [
    "SpacetimeFabricMetricInput.completed",
    "spacetime_fabric_metric_input_closed",
    "YtRGravityElasticRealDataEvidenceTarget",
]:
    assert token in lean_text

assert "import Chronos.Frontier.SpacetimeFabricMetricInput" in chronos_text

for token in [
    "(M, g)",
    "Lorentzian metric",
    "Einstein",
    "No literal spacetime fabric claim",
    "No new gravity claim",
    "No standard GR failure claim",
    "No Lambda-CDM failure claim",
    "No dark matter replacement claim",
    "No P vs NP",
    "No Clay problem",
]:
    assert token in doc_text

for token in [
    "literal gravity elasticity",
    "new gravity",
    "standard GR failure",
    "Lambda-CDM failure",
    "dark matter replacement",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in art_text

print("SPACETIME_FABRIC_METRIC_INPUT_OK")
