#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/qk_dini_source_derived_coefficient_family_interface_2026_06_09.json"
lean_file = ROOT / "lean/Chronos/Frontier/QKDiniSourceDerivedCoefficientFamilyInterface.lean"
status_doc = ROOT / "docs/status/QK_DINI_SOURCE_DERIVED_COEFFICIENT_FAMILY_INTERFACE_2026_06_09.md"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
lean_text = lean_file.read_text()
status_text = status_doc.read_text()
root_text = root_import.read_text()

assert data["object"] == "QKDiniSourceDerivedCoefficientFamilyInterface"
assert data["status"] == "SOURCE_DERIVED_COEFFICIENT_FAMILY_INTERFACE_ONLY"
assert data["minimal_missing_object"] == "ConcreteScientificQKDiniSourceObject"

required_lean_terms = [
    "structure QKDiniSourceObject",
    "def QKDiniSourceObject.toCoefficientFamily",
    "def QKDiniSourceObject.toUniformCoefficientBounds",
    "theorem qkDiniSourceObject_extracted_coefficient_nonzero",
    "theorem qkDiniSourceObject_extracted_uniform_bound",
]
for term in required_lean_terms:
    assert term in lean_text

assert "axiom " not in lean_text
assert "sorry" not in lean_text

for boundary in [
    "NO_CONCRETE_SCIENTIFIC_QK_DINI_SOURCE_OBJECT",
    "NO_ANALYTIC_DINI_ESTIMATE_PROOF",
    "NO_FINAL_THEOREM_CLOSURE",
    "NO_FINAL_SCIENTIFIC_CLOSURE",
]:
    assert boundary in data["boundary"]

assert "interface only" in status_text.lower()
assert "import Chronos.Frontier.QKDiniSourceDerivedCoefficientFamilyInterface" in root_text

print("QK_DINI_SOURCE_DERIVED_COEFFICIENT_FAMILY_INTERFACE_OK")
