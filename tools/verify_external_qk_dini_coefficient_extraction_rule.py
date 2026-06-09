#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/external_qk_dini_coefficient_extraction_rule_2026_06_09.json"
lean_file = ROOT / "lean/Chronos/Frontier/ExternalQKDiniCoefficientExtractionRule.lean"
status_doc = ROOT / "docs/status/EXTERNAL_QK_DINI_COEFFICIENT_EXTRACTION_RULE_2026_06_09.md"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
lean_text = lean_file.read_text()
status_text = status_doc.read_text()
root_text = root_import.read_text()

assert data["object"] == "ExternalQKDiniCoefficientExtractionRule"
assert data["status"] == "COEFFICIENT_EXTRACTION_RULE_RECORDED_ONLY"
assert data["source_id"] == "DOI:10.1155/2022/8496249"
assert data["coefficient_symbol"] == "zeta_n"
assert "(q;q)_n" in data["extracted_rule"]
assert "(q^k;q)_n" in data["extracted_rule"]
assert data["nat_codomain_status"] == "NO_NAT_RULE_WITHOUT_DISCRETIZATION_OR_ABSOLUTE_VALUE_ENCODING"
assert data["minimal_missing_object"] == "ParameterRestrictedExternalQKDiniCoefficientBoundTheorem"

required_lean_terms = [
    "structure ExternalQKDiniCoefficientExtractionRuleData",
    "def ExternalQKDiniCoefficientExtractionRule",
    "theorem externalQKDiniCoefficientExtractionRule_source_id",
    "theorem externalQKDiniCoefficientExtractionRule_symbol",
    "theorem externalQKDiniCoefficientExtractionRule_nat_obstruction",
    "theorem externalQKDiniCoefficientExtractionRule_uniform_bound_missing",
]
for term in required_lean_terms:
    assert term in lean_text

assert "axiom " not in lean_text
assert "sorry" not in lean_text

for boundary in [
    "COEFFICIENT_EXTRACTION_RULE_RECORDED_ONLY",
    "NO_FORMAL_COMPLEX_Q_CALCULUS_ENCODING",
    "NO_NAT_RULE_WITHOUT_DISCRETIZATION_OR_ABSOLUTE_VALUE_ENCODING",
    "NO_NONZERO_COEFFICIENT_PROOF_FROM_SOURCE",
    "NO_UNIFORM_BOUND_PROOF_FROM_SOURCE",
    "NO_EXTERNAL_QK_DINI_PAYLOAD_VALUE",
    "NO_ANALYTIC_DINI_ESTIMATE_PROOF",
    "NO_FINAL_THEOREM_CLOSURE",
    "NO_FINAL_SCIENTIFIC_CLOSURE",
]:
    assert boundary in data["boundary"]

assert "coefficient extraction rule recorded only" in status_text.lower()
assert "import Chronos.Frontier.ExternalQKDiniCoefficientExtractionRule" in root_text

print("EXTERNAL_QK_DINI_COEFFICIENT_EXTRACTION_RULE_OK")
