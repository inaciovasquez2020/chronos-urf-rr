import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/coordinate_or_row_binding_certificate_2026_06_01.json")
DOC = Path("docs/status/COORDINATE_OR_ROW_BINDING_CERTIFICATE_2026_06_01.md")
VERIFY = Path("tools/verify_coordinate_or_row_binding_certificate.py")

def test_artifact_records_coordinate_row_binding():
    data = json.loads(ART.read_text())
    assert data["object"] == "COORDINATE_OR_ROW_BINDING_CERTIFICATE"
    assert data["decision"] == "PASS"
    assert data["resolved_missing_input"] == "coordinate_or_row_binding_certificate"

def test_netcdf_metadata_is_bound():
    data = json.loads(ART.read_text())
    assert data["netcdf_dimensions"]
    assert data["coordinate_variables"]
    assert data["data_variables"]
    assert data["variable_bindings"]
    assert data["row_binding_rule"]["kind"] == "netCDF dimension-order binding"

def test_remaining_missing_inputs_are_five():
    data = json.loads(ART.read_text())
    assert data["remaining_missing_input_count"] == 5
    assert "baseline_gravity_vector" in data["remaining_missing_inputs"]
    assert "reproducible_comparison_run_output" in data["remaining_missing_inputs"]

def test_doc_preserves_boundary():
    doc = DOC.read_text()
    assert "coordinate and row binding only" in doc
    assert "no empirical gravity result supplied" in doc
    assert "no Clay-problem claim" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "COORDINATE_OR_ROW_BINDING_CERTIFICATE_OK" in result.stdout
