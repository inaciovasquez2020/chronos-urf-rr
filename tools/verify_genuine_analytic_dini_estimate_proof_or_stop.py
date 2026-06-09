#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/genuine_analytic_dini_estimate_proof_or_stop_2026_06_09.json"
LEAN = ROOT / "lean/Chronos/Frontier/GenuineAnalyticDiniEstimateProofOrStop.lean"
DOC = ROOT / "docs/status/GENUINE_ANALYTIC_DINI_ESTIMATE_PROOF_OR_STOP_2026_06_09.md"

REQUIRED_BOUNDARY = {
    "REPOSITORY_LOCAL_ENVELOPE_ALREADY_CLOSED",
    "GENUINE_ANALYTIC_DINI_ESTIMATE_PROOF_NOT_SUPPLIED",
    "NO_CONVERGENCE_CLAIM",
    "NO_SUMMABILITY_CLAIM",
    "NO_FINAL_ANALYTIC_RESULT",
    "NO_P_VS_NP_CLAIM",
    "NO_CLAY_CLAIM",
}

REQUIRED_LEAN = [
    "GenuineAnalyticDiniEstimateProofFrontierStatus",
    "requiresGenuineAnalyticDiniEstimateProof",
    "GenuineAnalyticDiniEstimateProofMinimalMissingObject",
    "GENUINE_ANALYTIC_DINI_ESTIMATE_PROOF",
    "GenuineAnalyticDiniEstimateProofBoundary",
]

def main() -> int:
    data = json.loads(ARTIFACT.read_text())
    lean = LEAN.read_text()
    doc = DOC.read_text()

    assert data["status"] == "STOPPED_AT_REPOSITORY_LOCAL_ENVELOPE"
    assert data["closed_prior_object"] == "analyticDiniEstimateBindingLemma"
    assert data["minimal_missing_object"] == "GENUINE_ANALYTIC_DINI_ESTIMATE_PROOF"
    assert data["next_admissible_object"] == "GENUINE_ANALYTIC_DINI_ESTIMATE_PROOF"
    assert REQUIRED_BOUNDARY.issubset(set(data["boundary"]))

    for needle in REQUIRED_LEAN:
        assert needle in lean

    assert "STOPPED_AT_REPOSITORY_LOCAL_ENVELOPE" in doc
    assert "GENUINE_ANALYTIC_DINI_ESTIMATE_PROOF" in doc

    print("GENUINE_ANALYTIC_DINI_ESTIMATE_PROOF_OR_STOP_OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
