#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/parameter_restricted_external_qk_dini_coefficient_bound_2026_06_09.json"
lean_file = ROOT / "lean/Chronos/Frontier/ParameterRestrictedExternalQKDiniCoefficientBound.lean"
status_doc = ROOT / "docs/status/PARAMETER_RESTRICTED_EXTERNAL_QK_DINI_COEFFICIENT_BOUND_2026_06_09.md"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
lean_text = lean_file.read_text()
status_text = status_doc.read_text()
root_text = root_import.read_text()

assert data["object"] == "ParameterRestrictedExternalQKDiniCoefficientBoundTheorem"
assert data["status"] == "CONDITIONAL_PARAMETER_RESTRICTED_BOUND_THEOREM_ONLY"
assert data["source_id"] == "DOI:10.1155/2022/8496249"
assert data["coefficient_symbol"] == "zeta_n"
assert data["analytic_codomain"] == "Real"
assert data["minimal_missing_object"] == "ConcreteParameterRestrictedExternalQKDiniCoefficientSliceValue"

required_lean_terms = [
    "noncomputable def qPochhammerReal",
    "noncomputable def externalQKDiniNumerator",
    "noncomputable def externalQKDiniDenominator",
    "noncomputable def externalQKDiniCoefficient",
    "structure ParameterRestrictedExternalQKDiniCoefficientSlice",
    "theorem externalQKDiniCoefficient_zero_eq_one",
    "theorem parameterRestrictedExternalQKDiniCoefficient_nonzero_witness",
    "theorem parameterRestrictedExternalQKDiniCoefficient_denominator_nonzero",
    "theorem parameterRestrictedExternalQKDiniCoefficientBoundTheorem",
]
for term in required_lean_terms:
    assert term in lean_text

assert "denominator_nonzero :" in lean_text
assert "coefficient_abs_bound :" in lean_text
assert "axiom " not in lean_text
assert "sorry" not in lean_text

for boundary in [
    "CONDITIONAL_PARAMETER_RESTRICTED_BOUND_ONLY",
    "REAL_SCALAR_ENCODING_ONLY",
    "DENOMINATOR_NONZERO_REQUIRES_PARAMETER_RESTRICTION_FIELD",
    "UNIFORM_BOUND_REQUIRES_PARAMETER_RESTRICTION_FIELD",
    "NO_CONCRETE_PARAMETER_SLICE_VALUE",
    "NO_UNCONDITIONAL_ANALYTIC_DINI_ESTIMATE_PROOF",
    "NO_FINAL_THEOREM_CLOSURE",
    "NO_FINAL_SCIENTIFIC_CLOSURE",
]:
    assert boundary in data["boundary"]

assert "conditional parameter-restricted bound only" in status_text.lower()
assert "import Chronos.Frontier.ParameterRestrictedExternalQKDiniCoefficientBound" in root_text

print("PARAMETER_RESTRICTED_EXTERNAL_QK_DINI_COEFFICIENT_BOUND_OK")
