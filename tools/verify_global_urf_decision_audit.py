#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/global_urf_decision_audit_2026_05_18.json"
DOC = ROOT / "docs/status/GLOBAL_URF_DECISION_AUDIT_2026_05_18.md"
LEAN = ROOT / "lean/Chronos/Frontier/GlobalURFDecisionAudit.lean"

REQUIRED_BOUNDARY = [
    "Does not prove unrestricted UniversalFiberEntropyGap.",
    "Does not prove unrestricted Chronos-RR.",
    "Does not prove unrestricted H4.1/FGL.",
    "Does not prove P vs NP.",
    "Does not prove any Clay problem.",
]

FORBIDDEN_DOC_OR_LEAN = [
    "unrestricted UniversalFiberEntropyGap is proved",
    "unrestricted Chronos-RR is proved",
    "unrestricted H4.1/FGL is proved",
    "P vs NP is proved",
    "Clay problem is solved",
    "Clay problems are solved",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()
    lean = LEAN.read_text()

    assert data["status"] == "STATUS_SURFACE_ONLY"
    assert data["global_verdict"] == "OPEN_WITH_EXPLICIT_SINK_LEMMAS"

    claims = data["claims"]
    assert len(claims) >= 4
    assert all(c["form"] == "A_i => B_i" for c in claims)
    assert all(c["A_i"] and c["B_i"] for c in claims)
    assert all("lean_proof_target" in c for c in claims)
    assert all("countermodel_target" in c for c in claims)
    assert all("sink_lemma" in c for c in claims)

    assert any(c["verdict"] == "proved_surface" for c in claims)
    assert any(c["verdict"] == "conditional_surface" for c in claims)
    assert any(c["verdict"] == "countermodel_required" for c in claims)
    assert any(c["verdict"] == "open_missing_lemma" for c in claims)

    sinks = data["dependency_dag_sinks"]
    assert "unrestricted uniform positivity/coercivity" in sinks
    assert "unrestricted UniversalFiberEntropyGap plus unrestricted DepthBridge" in sinks

    for line in REQUIRED_BOUNDARY:
        assert line in data["boundary"]

    for token in FORBIDDEN_DOC_OR_LEAN:
        assert token not in doc
        assert token not in lean

    assert "globalURFDecisionAudit_status_lock" in lean
    assert "globalURFDecisionAudit_nonempty" in lean
    assert "sorry" not in lean
    assert "admit" not in lean

    print("Global URF decision audit verified.")

if __name__ == "__main__":
    main()
