#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "Chronos/Frontier/SelectedCarrierNontrivialCountingFrontier.lean"
ROOT_LEAN = ROOT / "Chronos.lean"
JSON_PATH = ROOT / "artifacts/chronos/selected_carrier_nontrivial_counting_frontier.json"
DOC = ROOT / "docs/status/CHRONOS_SELECTED_CARRIER_NONTRIVIAL_COUNTING_FRONTIER_2026_05_09.md"

for path in [LEAN, ROOT_LEAN, JSON_PATH, DOC]:
    assert path.exists(), f"missing required file: {path}"

lean = LEAN.read_text()
root_lean = ROOT_LEAN.read_text()
doc = DOC.read_text()
json_text = JSON_PATH.read_text()
data = json.loads(json_text)

assert data["status"] == "FRONTIER_OPEN"
assert data["frontier"] == "SELECTED_CARRIER_NONTRIVIAL_COUNTING_MODEL_MISSING"
assert data["missing_object"] == "SelectedCarrierNontrivialDimensionExtraction"
assert data["lean_file"] == "Chronos/Frontier/SelectedCarrierNontrivialCountingFrontier.lean"

required_lean = [
    "def SelectedCarrierNontrivialCountingModelMissing",
    "theorem selected_carrier_nontrivial_counting_model_missing_recorded",
    "def NoClosurePromotionFromSelectedCarrierCountingFrontier",
    "theorem no_closure_promotion_from_selected_carrier_counting_frontier",
]
for token in required_lean:
    assert token in lean, f"missing Lean token: {token}"

assert "import Chronos.Frontier.SelectedCarrierNontrivialCountingFrontier" in root_lean

for bad in ["axiom", "constant", "sorry", "admit"]:
    assert not re.search(rf"\b{bad}\b", lean), f"forbidden Lean token in new file: {bad}"

required_doc = [
    "STATUS: FRONTIER_OPEN / SELECTED_CARRIER_NONTRIVIAL_COUNTING_MODEL_MISSING",
    "SelectedCarrierNontrivialDimensionExtraction",
    "TranscriptDim := fun _ _ => 0",
    "It does not encode invented transcript or observation dimensions.",
    "It does not assert unrestricted Chronos-RR closure.",
    "It does not assert H4.1/FGL closure.",
    "It does not assert P-vs-NP closure.",
    "It does not assert Clay-problem closure.",
    "It does not assert universal FiberEntropyGap.",
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

print("SelectedCarrierNontrivialCounting frontier verified: FRONTIER_OPEN")
