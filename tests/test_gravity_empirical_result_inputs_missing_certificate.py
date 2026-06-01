import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/gravity_empirical_result_inputs_missing_certificate_2026_06_01.json")
DOC = Path("docs/status/GRAVITY_EMPIRICAL_RESULT_INPUTS_MISSING_CERTIFICATE_2026_06_01.md")
VERIFY = Path("tools/verify_gravity_empirical_result_inputs_missing_certificate.py")

def test_artifact_records_missing_inputs_status():
    data = json.loads(ART.read_text())
    assert data["object"] == "GRAVITY_EMPIRICAL_RESULT_INPUTS_MISSING_CERTIFICATE"
    assert data["status"] == "EXPLICIT_EMPIRICAL_INPUTS_MISSING_NO_RESULT_SUPPLIED"
    assert data["decision"] == "PASS"

def test_all_empirical_inputs_remain_missing():
    data = json.loads(ART.read_text())
    assert data["empirical_gravity_result_supplied"] is False
    assert data["authenticated_gravity_payload_supplied"] is False
    assert data["baseline_gravity_vector_supplied"] is False
    assert data["model_or_deficit_mass_vector_supplied"] is False
    assert data["reproducible_comparison_run_output_supplied"] is False

def test_missing_input_set_is_complete():
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

def test_doc_records_boundary():
    doc = DOC.read_text()
    assert "no empirical gravity result supplied" in doc
    assert "no DFM-MKC validation" in doc
    assert "no Clay-problem claim" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "GRAVITY_EMPIRICAL_RESULT_INPUTS_MISSING_CERTIFICATE_OK" in result.stdout
