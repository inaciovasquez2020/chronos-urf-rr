#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/global_urf_next_level_targets_2026_05_18.json"
DOC = ROOT / "docs/status/GLOBAL_URF_NEXT_LEVEL_TARGETS_2026_05_18.md"

FORBIDDEN = [
    "P vs NP is solved",
    "Clay problem is solved",
    "unrestricted Chronos-RR is proved",
    "unrestricted H4.1/FGL is proved",
    "unrestricted UniversalFiberEntropyGap is proved",
    "NEXT_LEVEL_TARGET_SURFACE_ONLY proves",
]

REQUIRED_DOC_PHRASES = [
    "Status: `NEXT_LEVEL_TARGET_SURFACE_ONLY`",
    "Global verdict preserved: `OPEN`",
    "Does not prove:",
    "unrestricted `UniversalFiberEntropyGap`",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

def main() -> None:
    assert ARTIFACT.exists(), f"missing artifact: {ARTIFACT}"
    assert DOC.exists(), f"missing doc: {DOC}"

    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["status"] == "NEXT_LEVEL_TARGET_SURFACE_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False

    snap = data["snapshot_inputs"]
    assert snap["total_claims_tracked"] == 4
    assert snap["proved_surface_percent"] == 25
    assert snap["conditional_percent"] == 25
    assert snap["open_or_countermodel_needed_percent"] == 50
    assert snap["dependency_dag_sink_obstacles"] == 3
    assert snap["boundary_warnings"] == 5
    assert snap["post_numeric_snapshot_tests_passed"] == 961
    assert snap["post_dependency_dag_tests_passed"] == 964

    targets = data["ranked_next_targets"]
    assert len(targets) == 3
    assert [t["rank"] for t in targets] == [1, 2, 3]
    assert len({t["target_id"] for t in targets}) == 3

    for target in targets:
        assert target["status"] == "OPEN_TARGET"
        assert target["weakest_sufficient_next_ingredient"]
        assert target["blocks"]
        assert target["nonclaim"]

    boundary = data["boundary"]["does_not_prove"]
    for phrase in [
        "unrestricted UniversalFiberEntropyGap",
        "unrestricted Chronos-RR",
        "unrestricted H4.1/FGL",
        "P vs NP",
        "any Clay problem",
    ]:
        assert phrase in boundary

    for phrase in REQUIRED_DOC_PHRASES:
        assert phrase in doc

    combined = json.dumps(data, sort_keys=True) + "\n" + doc
    for phrase in FORBIDDEN:
        assert phrase not in combined

    print("Global URF next-level targets verified.")

if __name__ == "__main__":
    main()
