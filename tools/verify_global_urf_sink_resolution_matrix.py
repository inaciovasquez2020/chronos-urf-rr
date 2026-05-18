#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/global_urf_sink_resolution_matrix_2026_05_18.json"
DOC = ROOT / "docs/status/GLOBAL_URF_SINK_RESOLUTION_MATRIX_2026_05_18.md"

FORBIDDEN = [
    "P vs NP is solved",
    "Clay problem is solved",
    "unrestricted Chronos-RR is proved",
    "unrestricted H4.1/FGL is proved",
    "unrestricted UniversalFiberEntropyGap is proved",
    "uniform positive fiber-mass floor is proved",
    "finite-support-to-admissible-domain lift is proved"
]

def main() -> None:
    assert ARTIFACT.exists(), f"missing artifact: {ARTIFACT}"
    assert DOC.exists(), f"missing doc: {DOC}"

    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["status"] == "SINK_RESOLUTION_MATRIX_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False
    assert data["source"] == "global_urf_next_level_targets_2026_05_18"

    matrix = data["sink_resolution_matrix"]
    assert len(matrix) == 3
    assert [row["rank"] for row in matrix] == [1, 2, 3]

    for row in matrix:
        assert row["current_status"] == "OPEN_TARGET"
        assert row["closure_exit"]["required_object"]
        assert row["closure_exit"]["minimal_form"]
        assert row["countermodel_exit"]["required_object"]
        assert row["countermodel_exit"]["minimal_form"]

    assert matrix[0]["closure_exit"]["required_object"] == "UniformPositiveFiberMassFloor"
    assert matrix[0]["countermodel_exit"]["required_object"] == "NoUniformPositiveFiberMassFloorCountermodel"

    required_doc = [
        "Status: `SINK_RESOLUTION_MATRIX_ONLY`",
        "Global verdict preserved: `OPEN`",
        "`UniformPositiveFiberMassFloor`",
        "`NoUniformPositiveFiberMassFloorCountermodel`",
        "Does not prove:",
        "unrestricted `UniversalFiberEntropyGap`",
        "unrestricted Chronos-RR",
        "unrestricted H4.1/FGL",
        "P vs NP",
        "any Clay problem"
    ]
    for phrase in required_doc:
        assert phrase in doc

    combined = json.dumps(data, sort_keys=True) + "\n" + doc
    for phrase in FORBIDDEN:
        assert phrase not in combined

    print("Global URF sink resolution matrix verified.")

if __name__ == "__main__":
    main()
