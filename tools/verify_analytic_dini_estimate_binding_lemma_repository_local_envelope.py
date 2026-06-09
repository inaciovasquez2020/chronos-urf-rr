#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/analytic_dini_estimate_binding_lemma_repository_local_envelope_2026_06_09.json"
LEAN = ROOT / "lean/Chronos/Frontier/AnalyticDiniEstimateBindingLemma.lean"
DOC = ROOT / "docs/status/ANALYTIC_DINI_ESTIMATE_BINDING_LEMMA_REPOSITORY_LOCAL_ENVELOPE_2026_06_09.md"

REQUIRED_LEAN_STRINGS = [
    "structure UniformCoefficientBound",
    "structure AnalyticDiniEstimate",
    "def RepositoryLocalUniformCoefficientBoundWitness",
    "def analyticDiniEstimate_from_uniformBound",
    "def analyticDiniEstimateBindingLemma",
    "_S : NondegenerateSourceValidExternalQKDiniCoefficientSlice",
    "repositoryLocalEnvelopeOnlyNoAnalyticClosure",
]

REQUIRED_BOUNDARY = {
    "REPOSITORY_LOCAL_ENVELOPE_ONLY",
    "NO_GENUINE_ANALYTIC_DINI_ESTIMATE",
    "NO_CONVERGENCE_CLAIM",
    "NO_SUMMABILITY_CLAIM",
    "NO_FINAL_ANALYTIC_RESULT",
    "NO_P_VS_NP_CLAIM",
    "NO_CLAY_CLAIM",
}

def main() -> int:
    data = json.loads(ARTIFACT.read_text())
    lean_text = LEAN.read_text()
    doc_text = DOC.read_text()

    assert data["status"] == "REPOSITORY_LOCAL_ENVELOPE_ONLY_NO_ANALYTIC_CLOSURE"
    assert data["closed_object"] == "analyticDiniEstimateBindingLemma"
    assert REQUIRED_BOUNDARY.issubset(set(data["boundary"]))

    for needle in REQUIRED_LEAN_STRINGS:
        assert needle in lean_text

    assert "NO_GENUINE_ANALYTIC_DINI_ESTIMATE" in doc_text
    assert "GENUINE_ANALYTIC_DINI_ESTIMATE_PROOF_OR_STOP" in doc_text

    print("ANALYTIC_DINI_ESTIMATE_BINDING_LEMMA_REPOSITORY_LOCAL_ENVELOPE_OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
