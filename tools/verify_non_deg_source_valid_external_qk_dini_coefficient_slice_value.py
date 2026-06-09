#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/nondegenerate_source_valid_external_qk_dini_coefficient_slice_value_2026_06_09.json"
LEAN = ROOT / "lean/Chronos/Frontier/NondegenerateSourceValidExternalQKDiniCoefficientSliceValue.lean"
DOC = ROOT / "docs/status/NONDEGENERATE_SOURCE_VALID_EXTERNAL_QK_DINI_COEFFICIENT_SLICE_VALUE_2026_06_09.md"

REQUIRED_LEAN_STRINGS = [
    "structure NondegenerateSourceValidExternalQKDiniCoefficientSlice",
    "def NondegenerateSourceValidExternalQKDiniCoefficientSliceValue",
    "c := 1 / 16",
    "q := 1 / 2",
    "denominator_nonzero",
    "theorem1_coefficient_condition",
    "theorem2_first_coefficient_condition",
    "theorem2_second_coefficient_condition",
    "sliceValueOnlyNoAnalyticDiniEstimateClosure",
]

REQUIRED_BOUNDARY = {
    "NONDEGENERATE_SLICE_VALUE_ONLY",
    "SOURCE_RESTRICTION_NUMERIC_CERTIFICATE_ONLY",
    "NO_UNCONDITIONAL_ANALYTIC_DINI_ESTIMATE_PROOF",
    "NO_FINAL_ANALYTIC_RESULT",
    "NO_P_VS_NP_CLAIM",
    "NO_CLAY_CLAIM",
}

def main() -> int:
    data = json.loads(ARTIFACT.read_text())
    lean_text = LEAN.read_text()
    doc_text = DOC.read_text()

    assert data["status"] == "SLICE_VALUE_ONLY_NO_ANALYTIC_DINI_ESTIMATE_CLOSURE"
    assert data["closed_object"] == "NondegenerateSourceValidExternalQKDiniCoefficientSliceValue"
    assert data["parameter_slice"]["c"] == "1/16"
    assert data["parameter_slice"]["q"] == "1/2"
    assert data["minimal_missing_object"] == "AnalyticDiniEstimateBindingLemma_OR_STOP"

    boundary = set(data["boundary"])
    assert REQUIRED_BOUNDARY.issubset(boundary)

    for needle in REQUIRED_LEAN_STRINGS:
        assert needle in lean_text

    assert "NO_UNCONDITIONAL_ANALYTIC_DINI_ESTIMATE_PROOF" in doc_text
    assert "AnalyticDiniEstimateBindingLemma_OR_STOP" in doc_text

    print("NONDEGENERATE_SOURCE_VALID_EXTERNAL_QK_DINI_COEFFICIENT_SLICE_VALUE_OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
