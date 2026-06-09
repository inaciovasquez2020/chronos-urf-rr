#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/qk_dini_ratio_lower_bound_theorem_interface_no_sorry_2026_06_09.json"
LEAN = ROOT / "lean/Chronos/Frontier/QKDiniRatioLowerBoundTheoremInterfaceNoSorry.lean"
DOC = ROOT / "docs/status/QK_DINI_RATIO_LOWER_BOUND_THEOREM_INTERFACE_NO_SORRY_2026_06_09.md"

REQUIRED_BOUNDARY = {
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
    "structure GenuineAnalyticDiniEstimate",
    "structure QKDiniRatioLowerBoundTheoremInterface",
    "source_theorem_supplies_statement",
    "def genuineAnalyticDiniEstimate_from_source_theorem",
    "conditionalExternalTheoremInterfaceOnly",
    "QKDiniRatioLowerBoundTheoremInterfaceNoSorryBoundary",
]

def main() -> int:
    data = json.loads(ARTIFACT.read_text())
    lean = LEAN.read_text()
    doc = DOC.read_text()

    assert data["status"] == "CONDITIONAL_EXTERNAL_THEOREM_INTERFACE_ONLY"
    assert data["closed_object"] == "QKDiniRatioLowerBoundTheoremInterface"
    assert data["closed_transport"] == "genuineAnalyticDiniEstimate_from_source_theorem"
    assert data["sorry_count"] == 0
    assert REQUIRED_BOUNDARY.issubset(set(data["boundary"]))
    assert re.search(r"(?<![A-Za-z0-9_])sorry(?![A-Za-z0-9_])", lean, re.IGNORECASE) is None

    for needle in REQUIRED_LEAN:
        assert needle in lean

    assert "SORRY_COUNT: 0" in doc
    assert "ExternalSourceTheoremCertificate" in doc

    print("QK_DINI_RATIO_LOWER_BOUND_THEOREM_INTERFACE_NO_SORRY_OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
