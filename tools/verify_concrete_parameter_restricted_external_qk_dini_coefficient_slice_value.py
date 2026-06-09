#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/concrete_parameter_restricted_external_qk_dini_coefficient_slice_value_2026_06_09.json"
lean_file = ROOT / "lean/Chronos/Frontier/ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue.lean"
status_doc = ROOT / "docs/status/CONCRETE_PARAMETER_RESTRICTED_EXTERNAL_QK_DINI_COEFFICIENT_SLICE_VALUE_2026_06_09.md"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
lean_text = lean_file.read_text()
status_text = status_doc.read_text()
root_text = root_import.read_text()

assert data["object"] == "ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue"
assert data["status"] == "CONCRETE_DEGENERATE_C_ZERO_PARAMETER_SLICE_VALUE_ONLY"
assert data["source_id"] == "DOI:10.1155/2022/8496249"
assert data["analytic_codomain"] == "Real"
assert data["parameter_slice"] == {
    "a": "1",
    "c": "0",
    "q": "1/2",
    "k": "1",
    "B": "1",
}
assert data["minimal_missing_object"] == "NondegenerateSourceValidExternalQKDiniCoefficientSliceValue"

required_lean_terms = [
    "lemma qPochhammerReal_half_one_pos",
    "def ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue",
    "theorem concreteParameterRestrictedExternalQKDiniCoefficientSliceValue_nonzero_witness",
    "theorem concreteParameterRestrictedExternalQKDiniCoefficientSliceValue_denominator_nonzero",
    "theorem concreteParameterRestrictedExternalQKDiniCoefficientSliceValue_bound",
]
for term in required_lean_terms:
    assert term in lean_text

assert "a := 1" in lean_text
assert "c := 0" in lean_text
assert "q := (1 / 2 : ℝ)" in lean_text
assert "k := 1" in lean_text
assert "B := 1" in lean_text
assert "axiom " not in lean_text
assert "sorry" not in lean_text

for boundary in [
    "CONCRETE_PARAMETER_SLICE_VALUE_ONLY",
    "DEGENERATE_C_ZERO_SLICE_ONLY",
    "REAL_SCALAR_ENCODING_ONLY",
    "NO_NONDEGENERATE_SOURCE_VALID_PARAMETER_SLICE",
    "NO_UNCONDITIONAL_ANALYTIC_DINI_ESTIMATE_PROOF",
    "NO_FINAL_THEOREM_CLOSURE",
    "NO_FINAL_SCIENTIFIC_CLOSURE",
]:
    assert boundary in data["boundary"]

assert "degenerate" in status_text.lower()
assert "import Chronos.Frontier.ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue" in root_text

print("CONCRETE_PARAMETER_RESTRICTED_EXTERNAL_QK_DINI_COEFFICIENT_SLICE_VALUE_OK")
