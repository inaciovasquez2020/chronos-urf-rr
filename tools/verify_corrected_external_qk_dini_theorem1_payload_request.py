from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT = ROOT / "artifacts/chronos/corrected_external_qk_dini_theorem1_payload_request_2026_06_10.json"
DOC = ROOT / "docs/status/CORRECTED_EXTERNAL_QK_DINI_THEOREM1_PAYLOAD_REQUEST_2026_06_10.md"
LEAN = ROOT / "lean/Chronos/Frontier/CorrectedExternalQKDiniRatioLowerBoundTheorem1.lean"

REQUIRED_BOUNDARY = {
    "no new axiom",
    "no repository-native analytic proof",
    "no extraction from printed Theorem 1 as-is",
    "transport closes only after GenuineAnalyticDiniEstimate is supplied",
}

def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")
    lean = LEAN.read_text(encoding="utf-8")

    assert data["status"] == "PAYLOAD_REQUIRED"
    assert data["object"] == "CorrectedExternalQKDiniRatioLowerBoundTheorem1PayloadRequest"
    assert data["minimal_missing_object"] == "payload : GenuineAnalyticDiniEstimate"
    assert data["closed_transport_surface"] == "CorrectedExternalQKDiniRatioLowerBoundTheorem1"
    assert set(data["boundary"]) == REQUIRED_BOUNDARY

    assert "SOURCE_ERRATUM_REQUIRED_EXTERNAL_QK_DINI_THEOREM1_2026_06_10" in data["depends_on"]
    assert "CorrectedExternalQKDiniRatioLowerBoundTheorem1" in data["depends_on"]

    assert "Status: PAYLOAD_REQUIRED." in doc
    assert "payload : GenuineAnalyticDiniEstimate" in doc
    assert "CorrectedExternalQKDiniRatioLowerBoundTheorem1" in doc
    assert "no new axiom" in doc

    assert "def CorrectedExternalQKDiniRatioLowerBoundTheorem1" in lean
    assert "(payload : GenuineAnalyticDiniEstimate)" in lean
    assert "axiom CorrectedExternalQKDiniRatioLowerBoundTheorem1" not in lean

    print("CORRECTED_EXTERNAL_QK_DINI_THEOREM1_PAYLOAD_REQUEST_OK")

if __name__ == "__main__":
    main()
