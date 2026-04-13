from pathlib import Path
import json


def test_per_step_info_bound_doc_lock():
    text = Path("docs/math/PER_STEP_INFORMATION_BOUND.md").read_text()
    assert "Status: PROVED" in text
    assert "info_leakage(s) <= V_C." in text
    assert "remaining information-side bound" in text
    assert "Per-Step Information Bound" in text


def test_info_leakage_artifact_lock():
    data = json.loads(Path("artifacts/info_leakage_stats.json").read_text())
    assert data["project"] == "chronos-urf-rr"
    assert data["metric"] == "InformationLeakage"
    assert data["status"] == "awaiting_verification"
    assert "theoretical_max" in data["bounds"]
