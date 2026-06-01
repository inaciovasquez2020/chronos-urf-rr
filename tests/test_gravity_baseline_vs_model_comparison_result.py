import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/gravity_baseline_vs_model_comparison_result_2026_06_01.json")
DOC = Path("docs/status/GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_2026_06_01.md")
VERIFY = Path("tools/verify_gravity_baseline_vs_model_comparison_result.py")

def test_artifact_exists_and_is_target_open():
    data = json.loads(ART.read_text())
    assert data["object"] == "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT"
    assert data["status"] == "TARGET_OPEN_COMPARISON_INPUTS_NOT_SUPPLIED"
    assert data["decision"] == "PASS"
    assert data["comparison_result_supplied"] is False

def test_all_required_inputs_remain_missing():
    data = json.loads(ART.read_text())
    required = {
        "authenticated_gravity_payload",
        "coordinate_or_row_binding_certificate",
        "baseline_gravity_vector",
        "model_or_deficit_mass_vector",
        "unit_conversion_certificate",
        "predeclared_comparison_metric",
        "reproducible_comparison_run_output",
    }
    assert required.issubset(set(data["missing_inputs"]))

def test_boundary_blocks_overclaims():
    data = json.loads(ART.read_text())
    boundary = set(data["boundary"])
    assert "no empirical comparison result supplied" in boundary
    assert "no DFM-MKC validation" in boundary
    assert "no Lambda-CDM failure" in boundary
    assert "no Clay-problem claim" in boundary

def test_status_doc_records_next_object():
    doc = DOC.read_text()
    assert "GRAVITY_RESULT_BOUNDARY_CERTIFICATE" in doc
    assert "TARGET_OPEN_COMPARISON_INPUTS_NOT_SUPPLIED" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_OK" in result.stdout
