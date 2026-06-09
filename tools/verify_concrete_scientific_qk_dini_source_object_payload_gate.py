#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/concrete_scientific_qk_dini_source_object_payload_gate_2026_06_09.json"
lean_file = ROOT / "lean/Chronos/Frontier/ConcreteScientificQKDiniSourceObjectPayloadGate.lean"
status_doc = ROOT / "docs/status/CONCRETE_SCIENTIFIC_QK_DINI_SOURCE_OBJECT_PAYLOAD_GATE_2026_06_09.md"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
lean_text = lean_file.read_text()
status_text = status_doc.read_text()
root_text = root_import.read_text()

assert data["object"] == "ConcreteScientificQKDiniSourceObjectPayloadGate"
assert data["status"] == "PAYLOAD_GATE_ONLY_NO_CONCRETE_SCIENTIFIC_SOURCE_SUPPLIED"
assert data["minimal_missing_object"] == "ConcreteScientificQKDiniSourceObjectPayloadValue"
assert data["conditional"] is True

required_lean_terms = [
    "structure ConcreteScientificQKDiniSourceObjectPayload",
    "def ConcreteScientificQKDiniSourceObject : Prop",
    "theorem concreteScientificQKDiniSourceObject_has_source_object",
    "def concreteScientificQKDiniSourceObject_extracts_coefficient_family",
    "def concreteScientificQKDiniSourceObject_extracts_uniform_bounds",
]
for term in required_lean_terms:
    assert term in lean_text

assert "scientific_derivation_claim : Prop" in lean_text
assert "axiom " not in lean_text
assert "sorry" not in lean_text

for boundary in [
    "NO_CONCRETE_SCIENTIFIC_QK_DINI_SOURCE_OBJECT_PAYLOAD_VALUE",
    "NO_SOURCE_PAYLOAD_SUPPLIED",
    "NO_PROVEN_SCIENTIFIC_DERIVATION",
    "NO_ANALYTIC_DINI_ESTIMATE_PROOF",
    "NO_FINAL_THEOREM_CLOSURE",
    "NO_FINAL_SCIENTIFIC_CLOSURE",
]:
    assert boundary in data["boundary"]

assert "payload gate only" in status_text.lower()
assert "import Chronos.Frontier.ConcreteScientificQKDiniSourceObjectPayloadGate" in root_text

print("CONCRETE_SCIENTIFIC_QK_DINI_SOURCE_OBJECT_PAYLOAD_GATE_OK")
