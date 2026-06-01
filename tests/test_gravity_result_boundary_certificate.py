import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/gravity_result_boundary_certificate_2026_06_01.json")
PRIOR = Path("artifacts/chronos/gravity_baseline_vs_model_comparison_result_2026_06_01.json")
DOC = Path("docs/status/GRAVITY_RESULT_BOUNDARY_CERTIFICATE_2026_06_01.md")
VERIFY = Path("tools/verify_gravity_result_boundary_certificate.py")

def test_certificate_artifact_status():
    data = json.loads(ART.read_text())
    assert data["object"] == "GRAVITY_RESULT_BOUNDARY_CERTIFICATE"
    assert data["status"] == "BOUNDARY_CERTIFICATE_FOR_TARGET_OPEN_COMPARISON"
    assert data["decision"] == "PASS"

def test_prior_is_target_open():
    prior = json.loads(PRIOR.read_text())
    assert prior["object"] == "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT"
    assert prior["status"] == "TARGET_OPEN_COMPARISON_INPUTS_NOT_SUPPLIED"
    assert prior["comparison_result_supplied"] is False

def test_certificate_preserves_non_claims():
    data = json.loads(ART.read_text())
    non_claims = set(data["certified_non_claims"])
    assert "no empirical comparison result" in non_claims
    assert "no DFM-MKC validation" in non_claims
    assert "no Lambda-CDM failure" in non_claims
    assert "no Clay-problem claim" in non_claims

def test_doc_records_next_admissible_object():
    doc = DOC.read_text()
    assert "GLOBAL_URF_LAW3_RESTRICTED_VALID_KERNEL_INSTANCE" in doc
    assert "TARGET_OPEN_COMPARISON_INPUTS_NOT_SUPPLIED" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "GRAVITY_RESULT_BOUNDARY_CERTIFICATE_OK" in result.stdout
