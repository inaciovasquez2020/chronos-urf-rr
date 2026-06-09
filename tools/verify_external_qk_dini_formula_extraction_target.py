#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/external_qk_dini_formula_extraction_target_2026_06_09.json"
lean_file = ROOT / "lean/Chronos/Frontier/ExternalQKDiniFormulaExtractionTarget.lean"
status_doc = ROOT / "docs/status/EXTERNAL_QK_DINI_FORMULA_EXTRACTION_TARGET_2026_06_09.md"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
lean_text = lean_file.read_text()
status_text = status_doc.read_text()
root_text = root_import.read_text()

assert data["object"] == "ExternalQKDiniFormulaExtractionTarget"
assert data["status"] == "FORMULA_TRANSCRIPTION_TARGET_ONLY"
assert data["source_id"] == "DOI:10.1155/2022/8496249"
assert data["source_formula_name"] == "normalized q-generalized Dini function"
assert data["coefficient_symbol"] == "zeta_n"
assert data["minimal_missing_object"] == "FormalizedExternalQKDiniCoefficientExtractionRule"

required_lean_terms = [
    "structure ExternalQKDiniFormulaExtractionTargetData",
    "def ExternalQKDiniFormulaExtractionTarget",
    "theorem externalQKDiniFormulaExtractionTarget_source_id",
    "theorem externalQKDiniFormulaExtractionTarget_series_formula_recorded",
    "theorem externalQKDiniFormulaExtractionTarget_status",
]
for term in required_lean_terms:
    assert term in lean_text

assert "axiom " not in lean_text
assert "sorry" not in lean_text

for boundary in [
    "FORMULA_TRANSCRIPTION_TARGET_ONLY",
    "NO_FORMAL_COMPLEX_Q_CALCULUS_ENCODING",
    "NO_FORMAL_ZETA_N_COEFFICIENT_RULE_AS_NAT",
    "NO_NONZERO_COEFFICIENT_PROOF_FROM_SOURCE",
    "NO_UNIFORM_BOUND_PROOF_FROM_SOURCE",
    "NO_EXTERNAL_QK_DINI_PAYLOAD_VALUE",
    "NO_ANALYTIC_DINI_ESTIMATE_PROOF",
    "NO_FINAL_THEOREM_CLOSURE",
    "NO_FINAL_SCIENTIFIC_CLOSURE",
]:
    assert boundary in data["boundary"]

assert "formula transcription target only" in status_text.lower()
assert "import Chronos.Frontier.ExternalQKDiniFormulaExtractionTarget" in root_text

print("EXTERNAL_QK_DINI_FORMULA_EXTRACTION_TARGET_OK")
