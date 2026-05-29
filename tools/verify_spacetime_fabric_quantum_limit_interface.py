#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/SpacetimeFabricQuantumLimitInterface.lean"
ART = ROOT / "artifacts/chronos/spacetime_fabric_quantum_limit_interface_2026_05_29.json"
DOC = ROOT / "docs/status/SPACETIME_FABRIC_QUANTUM_LIMIT_INTERFACE_2026_05_29.md"
CHRONOS = ROOT / "lean/Chronos.lean"

lean_text = LEAN.read_text()
art_text = ART.read_text()
doc_text = DOC.read_text()
chronos_text = CHRONOS.read_text()
data = json.loads(art_text)

required = [
    "classicalMetricInputRecorded",
    "quantumStateSpaceRecorded",
    "metricOperatorOrPathIntegralSlotRecorded",
    "planckScaleRegimeRecorded",
    "semiclassicalLimitRecorded",
    "classicalRecoveryMapRecorded",
    "einsteinEquationRecoveryConditionRecorded",
    "quantumCorrectionSlotRecorded",
    "expectationMetricBridgeRecorded",
    "stressEnergyExpectationBridgeRecorded",
    "boundaryPreserved",
]

lean_tokens = [
    "SpacetimeFabricQuantumLimitInterface.completed",
    "spacetime_fabric_quantum_limit_interface_closed",
    "SpacetimeFabricMetricInput",
]

doc_tokens = [
    "SpacetimeFabricMetricInput",
    "(M, g)",
    "quantumStateSpace",
    "metricOperatorOrPathIntegralSlot",
    "semiclassicalLimit",
    "classicalRecoveryMap",
    "No quantum gravity proof",
    "No unification of GR and quantum mechanics",
    "No spacetime discreteness claim",
    "No new physics claim",
    "No P vs NP",
    "No Clay problem",
]

art_tokens = [
    "quantum gravity",
    "unification of GR and quantum mechanics",
    "spacetime discreteness",
    "graviton existence",
    "string theory",
    "loop quantum gravity",
    "emergent spacetime",
    "standard GR failure",
    "Lambda-CDM failure",
    "dark matter replacement",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

assert data["id"] == "SPACETIME_FABRIC_QUANTUM_LIMIT_INTERFACE_2026_05_29"
assert data["object"] == "SpacetimeFabricQuantumLimitInterface"
assert data["status"] == "QUANTUM_GRAVITY_INTERFACE_ONLY_NO_QUANTUM_GRAVITY_PROOF"
assert all(token in lean_text for token in required)
assert all(token in art_text for token in required)
assert all(token in lean_text for token in lean_tokens)
assert "import Chronos.Frontier.SpacetimeFabricQuantumLimitInterface" in chronos_text
assert all(token in doc_text for token in doc_tokens)
assert all(token in art_text for token in art_tokens)

print("SPACETIME_FABRIC_QUANTUM_LIMIT_INTERFACE_OK")
