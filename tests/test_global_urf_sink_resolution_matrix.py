import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/global_urf_sink_resolution_matrix_2026_05_18.json"
DOC = ROOT / "docs/status/GLOBAL_URF_SINK_RESOLUTION_MATRIX_2026_05_18.md"

def test_sink_resolution_matrix_status():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "SINK_RESOLUTION_MATRIX_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False

def test_sink_resolution_matrix_has_three_ranked_rows():
    data = json.loads(ARTIFACT.read_text())
    matrix = data["sink_resolution_matrix"]
    assert len(matrix) == 3
    assert [row["rank"] for row in matrix] == [1, 2, 3]

def test_each_sink_has_closure_and_countermodel_exit():
    data = json.loads(ARTIFACT.read_text())
    for row in data["sink_resolution_matrix"]:
        assert row["closure_exit"]["required_object"]
        assert row["closure_exit"]["minimal_form"]
        assert row["countermodel_exit"]["required_object"]
        assert row["countermodel_exit"]["minimal_form"]

def test_first_sink_is_uniform_positive_mass_dichotomy():
    data = json.loads(ARTIFACT.read_text())
    first = data["sink_resolution_matrix"][0]
    assert first["sink_id"] == "uniform_positive_mass_or_countermodel"
    assert first["closure_exit"]["required_object"] == "UniformPositiveFiberMassFloor"
    assert first["countermodel_exit"]["required_object"] == "NoUniformPositiveFiberMassFloorCountermodel"

def test_sink_resolution_matrix_boundaries():
    doc = DOC.read_text()
    assert "Does not prove:" in doc
    assert "uniform positive fiber-mass floor" in doc
    assert "finite-support-to-admissible-domain lift" in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "unrestricted Chronos-RR" in doc
    assert "unrestricted H4.1/FGL" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
