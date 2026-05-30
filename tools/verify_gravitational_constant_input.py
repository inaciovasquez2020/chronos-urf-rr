#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/GravitationalConstantInput.lean"
ART = ROOT / "artifacts/chronos/gravitational_constant_input_2026_05_29.json"
DOC = ROOT / "docs/status/GRAVITATIONAL_CONSTANT_INPUT_2026_05_29.md"
CHRONOS = ROOT / "lean/Chronos.lean"

lean_text = LEAN.read_text()
art_text = ART.read_text()
doc_text = DOC.read_text()
chronos_text = CHRONOS.read_text()
data = json.loads(art_text)

required = [
    "gravitationalConstantSymbolRecorded",
    "codataValueRecorded",
    "codataSourceRecorded",
    "siUnitRecorded",
    "standardUncertaintyRecorded",
    "relativeUncertaintyRecorded",
    "newtonianForceUseRecorded",
    "einsteinCouplingUseRecorded",
    "notFittedParameterBoundaryRecorded",
    "noVaryingGClaimBoundaryRecorded",
    "boundaryPreserved",
]

doc_tokens = [
    "G = 6.67430e-11 m^3 kg^-1 s^-2",
    "standard uncertainty = 0.00015e-11 m^3 kg^-1 s^-2",
    "F = G m_1 m_2 / r^2",
    "G_{mu nu} + Lambda g_{mu nu} = (8 pi G / c^4) T_{mu nu}",
    "No new measurement of G.",
    "No derivation of G.",
    "No varying-G claim.",
    "No new gravity claim.",
    "No P vs NP.",
    "No Clay problem.",
]

art_tokens = [
    "6.67430e-11",
    "m^3 kg^-1 s^-2",
    "0.00015e-11",
    "2.2e-5",
    "new measurement of G",
    "derivation of G",
    "varying-G theory",
    "quantum gravity",
    "standard GR failure",
    "Lambda-CDM failure",
    "dark matter replacement",
    "any Clay problem",
]

assert data["id"] == "GRAVITATIONAL_CONSTANT_INPUT_2026_05_29"
assert data["object"] == "GravitationalConstantInput"
assert data["status"] == "PHYSICAL_CONSTANT_INPUT_ONLY_NO_NEW_G_MEASUREMENT"
assert all(token in lean_text for token in required)
assert all(token in art_text for token in required)
assert all(token in doc_text for token in required)
assert "GravitationalConstantInput.completed" in lean_text
assert "gravitational_constant_input_closed" in lean_text
assert "import Chronos.Frontier.GravitationalConstantInput" in chronos_text
assert all(token in doc_text for token in doc_tokens)
assert all(token in art_text for token in art_tokens)

print("GRAVITATIONAL_CONSTANT_INPUT_OK")
