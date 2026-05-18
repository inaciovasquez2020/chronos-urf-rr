import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/global_urf_next_level_targets_2026_05_18.json"
DOC = ROOT / "docs/status/GLOBAL_URF_NEXT_LEVEL_TARGETS_2026_05_18.md"

def test_next_level_targets_status_and_snapshot_numbers():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "NEXT_LEVEL_TARGET_SURFACE_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False
    assert data["snapshot_inputs"] == {
        "total_claims_tracked": 4,
        "proved_surface_percent": 25,
        "conditional_percent": 25,
        "open_or_countermodel_needed_percent": 50,
        "dependency_dag_sink_obstacles": 3,
        "boundary_warnings": 5,
        "post_numeric_snapshot_tests_passed": 961,
        "post_dependency_dag_tests_passed": 964,
    }

def test_next_level_targets_rank_three_open_targets():
    data = json.loads(ARTIFACT.read_text())
    targets = data["ranked_next_targets"]
    assert len(targets) == 3
    assert [target["rank"] for target in targets] == [1, 2, 3]
    assert all(target["status"] == "OPEN_TARGET" for target in targets)
    assert {target["target_id"] for target in targets} == {
        "uniform_positive_mass_or_countermodel",
        "domain_lift_from_finite_support",
        "countermodel_or_closure_dichotomy",
    }

def test_next_level_targets_preserve_boundaries():
    doc = DOC.read_text()
    assert "Does not prove:" in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "unrestricted Chronos-RR" in doc
    assert "unrestricted H4.1/FGL" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc

def test_next_level_targets_no_forbidden_overclaim_tokens():
    text = ARTIFACT.read_text() + "\n" + DOC.read_text()
    forbidden = [
        "P vs NP is solved",
        "Clay problem is solved",
        "unrestricted Chronos-RR is proved",
        "unrestricted H4.1/FGL is proved",
        "unrestricted UniversalFiberEntropyGap is proved",
    ]
    for phrase in forbidden:
        assert phrase not in text
