from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT = ROOT / "artifacts/chronos/source_erratum_required_external_qk_dini_theorem1_2026_06_10.json"
DOC = ROOT / "docs/status/SOURCE_ERRATUM_REQUIRED_EXTERNAL_QK_DINI_THEOREM1_2026_06_10.md"

REQUIRED_BOUNDARY = {
    "no GenuineAnalyticDiniEstimate extracted from printed Theorem 1 as-is",
    "no final analytic result",
    "no P vs NP claim",
    "no Clay claim",
}

def main() -> None:
    if not ARTIFACT.is_file():
        raise SystemExit(f"missing artifact: {ARTIFACT}")
    if not DOC.is_file():
        raise SystemExit(f"missing doc: {DOC}")

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["status"] == "BLOCKED_SOURCE_ERRATUM_REQUIRED"
    assert data["source_id"] == "DOI:10.1155/2022/8496249"
    assert data["blocked_object"] == "EXTERNAL_GENUINE_ANALYTIC_DINI_ESTIMATE_PAYLOAD"
    assert data["minimal_missing_lemma"] == "CorrectedExternalQKDiniRatioLowerBoundTheorem1"

    reason = data["reason"]
    assert "beta_1" in reason
    assert "exceeds 1" in reason
    assert "nondegenerate c != 0" in reason
    assert "psi/psi_m tends to 1" in reason

    assert set(data["boundary"]) == REQUIRED_BOUNDARY

    assert "# Source Erratum Required: External QK Dini Theorem 1" in doc
    assert "Status: BLOCKED." in doc
    assert "CorrectedExternalQKDiniRatioLowerBoundTheorem1" in doc
    assert "GenuineAnalyticDiniEstimate" in doc
    assert "beta_1 > 1" in doc
    assert "c != 0" in doc
    assert "psi/psi_m" in doc
    assert "No GenuineAnalyticDiniEstimate is extracted" in doc

    print("SOURCE_ERRATUM_REQUIRED_EXTERNAL_QK_DINI_THEOREM1_OK")

if __name__ == "__main__":
    main()
