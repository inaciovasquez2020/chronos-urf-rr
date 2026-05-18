#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "artifacts/chronos/global_urf_decision_audit_numeric_snapshot_2026_05_18.json"
DOC = ROOT / "docs/status/GLOBAL_URF_DECISION_AUDIT_NUMERIC_SNAPSHOT_2026_05_18.md"

def main() -> None:
    data = json.loads(SNAPSHOT.read_text())
    doc = DOC.read_text()

    assert data["artifact"] == "global_urf_decision_audit_numeric_snapshot"
    assert data["source_status"] == "STATUS_SURFACE_ONLY"
    assert data["global_verdict"] == "OPEN_WITH_EXPLICIT_SINK_LEMMAS"

    assert data["claims_total"] == 4
    assert data["proved_surface_count"] == 1
    assert data["conditional_surface_count"] == 1
    assert data["countermodel_required_count"] == 1
    assert data["open_missing_lemma_count"] == 1
    assert data["open_or_countermodel_count"] == 2

    assert data["proved_surface_percent"] == 25.0
    assert data["conditional_surface_percent"] == 25.0
    assert data["countermodel_required_percent"] == 25.0
    assert data["open_missing_lemma_percent"] == 25.0
    assert data["open_or_countermodel_percent"] == 50.0

    assert data["dependency_dag_sink_count"] == 3
    assert data["boundary_item_count"] == 5
    assert data["latest_full_pytest_passed"] == 958

    assert "NUMERIC_SNAPSHOT_ONLY" in doc
    assert "Does not prove:" in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc

    forbidden = [
        "proves unrestricted UniversalFiberEntropyGap",
        "proves unrestricted Chronos-RR",
        "proves unrestricted H4.1/FGL",
        "proves P vs NP",
        "proves any Clay problem",
        "Clay problem solved",
    ]
    for token in forbidden:
        assert token not in doc

    print("Global URF decision audit numeric snapshot verified.")

if __name__ == "__main__":
    main()
