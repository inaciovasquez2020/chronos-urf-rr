#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/external_source_theorem_certificate_one_axiom_2026_06_09.json"
LEAN = ROOT / "lean/Chronos/Frontier/ExternalSourceTheoremCertificateOneAxiom.lean"
DOC = ROOT / "docs/status/EXTERNAL_SOURCE_THEOREM_CERTIFICATE_ONE_AXIOM_2026_06_09.md"

REQUIRED_BOUNDARY = {
    "SORRY_COUNT_0",
    "AXIOM_COUNT_0",
    "EXTERNAL_PAYLOAD_REQUIRED",
    "CONDITIONAL_EXTERNAL_THEOREM_INTERFACE_ONLY",
    "NO_INTERNAL_ANALYTIC_PROOF",
    "NO_CONVERGENCE_PROOF",
    "NO_SUMMABILITY_PROOF",
    "NO_RATIO_BOUND_PROOF",
    "NO_FINAL_ANALYTIC_RESULT",
    "NO_P_VS_NP_CLAIM",
    "NO_CLAY_CLAIM",
}

REQUIRED_LEAN = [
    "structure ExternalSourceTheoremCertificate",
    "def externalSourceTheoremCertificate_to_genuineAnalyticDiniEstimate",
    "noncomputable def El_Qadeem_2022_Certificate",
    "noncomputable def genuineAnalyticDiniEstimate_from_El_Qadeem_2022",
    "payload : GenuineAnalyticDiniEstimate",
    "AXIOM_COUNT_0",
    "EXTERNAL_PAYLOAD_REQUIRED",
]

def main() -> int:
    data = json.loads(ARTIFACT.read_text())
    lean = LEAN.read_text()
    doc = DOC.read_text()

    assert data["status"] == "CONDITIONAL_EXTERNAL_THEOREM_CERTIFICATE_PAYLOAD_REQUIRED"
    assert data["closed_object"] == "ExternalSourceTheoremCertificate"
    assert data["sorry_count"] == 0
    assert data["axiom_count"] == 0
    assert data["payload_required"] == "GenuineAnalyticDiniEstimate"
    assert REQUIRED_BOUNDARY.issubset(set(data["boundary"]))

    assert re.search(r"(?<![A-Za-z0-9_])sorry(?![A-Za-z0-9_])", lean, re.IGNORECASE) is None
    assert re.search(r"(?<![A-Za-z0-9_])axiom(?![A-Za-z0-9_])", lean, re.IGNORECASE) is None

    for needle in REQUIRED_LEAN:
        assert needle in lean

    assert "SORRY_COUNT: 0" in doc
    assert "AXIOM_COUNT: 0" in doc
    assert "PAYLOAD_REQUIRED" in doc

    print("EXTERNAL_SOURCE_THEOREM_CERTIFICATE_PAYLOAD_REQUIRED_OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
