#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "Chronos/Frontier/SelectedCarrierEntropyFunctional.lean"
ROOT_LEAN = ROOT / "Chronos.lean"
JSON_PATH = ROOT / "artifacts/chronos/selected_carrier_entropy_functional.json"
DOC = ROOT / "docs/status/CHRONOS_SELECTED_CARRIER_ENTROPY_FUNCTIONAL_2026_05_09.md"

for path in [LEAN, ROOT_LEAN, JSON_PATH, DOC]:
    assert path.exists(), f"missing required file: {path}"

lean = LEAN.read_text()
root_lean = ROOT_LEAN.read_text()
doc = DOC.read_text()
json_text = JSON_PATH.read_text()
data = json.loads(json_text)

assert data["status"] == "SELECTED_CARRIER_ONLY_VERIFIED_SURFACE"
assert data["lean_file"] == "Chronos/Frontier/SelectedCarrierEntropyFunctional.lean"
assert data["theorem"] == "selected_carrier_entropy_functional_verified_surface"

required_lean = [
    "def SelectedCarrierEntropyFunctional",
    "def SelectedCarrierEntropyFunctionalClosed",
    "theorem selected_carrier_entropy_functional_closed",
    "def SelectedCarrierEntropyFunctionalVerifiedSurface",
    "theorem selected_carrier_entropy_functional_verified_surface",
    "SelectedCarrierFiberEntropyGap",
    "SelectedCarrierDepthBridgeInstance.TranscriptDim",
    "SelectedCarrierDepthBridgeInstance.ObsDim",
]

for token in required_lean:
    assert token in lean, f"missing Lean token: {token}"

for token in ["<<<<<<<", "=======", ">>>>>>>"]:
    assert token not in root_lean, f"merge conflict marker remains in Chronos.lean: {token}"

assert "import Chronos.Frontier.SelectedCarrierEntropyFunctional" in root_lean

for bad in ["axiom", "constant", "sorry", "admit"]:
    assert not re.search(rf"\b{bad}\b", lean), f"forbidden Lean token in new file: {bad}"

required_doc = [
    "STATUS: SELECTED_CARRIER_ONLY_VERIFIED_SURFACE",
    "selected repository-native positive-arity carrier domain",
    "selected_carrier_entropy_functional_verified_surface",
    "does not assert theorem-level Chronos-RR, H4.1/FGL, P-vs-NP, or Clay-problem closure",
    "No unrestricted admissible-predicate result is claimed.",
    "No universal FiberEntropyGap result is claimed.",
]

for token in required_doc:
    assert token in doc, f"missing status-doc token: {token}"

for text in [doc, json_text]:
    forbidden_positive_claims = [
        "P vs NP solved",
        "Clay solved",
        "Chronos-RR closed",
        "H4.1/FGL closed",
        "unrestricted theorem-level closure",
        "full theorem closure",
    ]
    for phrase in forbidden_positive_claims:
        assert phrase not in text, f"forbidden overclaim phrase: {phrase}"

print("SelectedCarrierEntropyFunctional verified: SELECTED_CARRIER_ONLY_VERIFIED_SURFACE")
