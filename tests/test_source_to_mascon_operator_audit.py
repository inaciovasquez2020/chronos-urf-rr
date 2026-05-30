import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/source_to_mascon_operator_audit_2026_05_30.json"

def test_source_to_mascon_operator_audit_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_source_to_mascon_operator_audit.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "SOURCE_TO_MASCON_OPERATOR_AUDIT_OK" in result.stdout

def test_source_to_mascon_operator_audit_boundaries():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    audit = artifact["audit"]
    assert audit["mascon_unit_equivalence_closed"] is False
    assert audit["time_dependent_source_to_mascon_operator_closed"] is False
    assert audit["empirical_gravity_result_claimed"] is False
    assert audit["dark_matter_replacement_claimed"] is False
    assert audit["lambda_cdm_failure_claimed"] is False

def test_source_to_mascon_operator_audit_next_object():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    assert artifact["next_admissible_object"] == (
        "MASCON_UNIT_EQUIVALENCE_CERTIFICATE_OR_TIME_DEPENDENT_SOURCE_TO_MASCON_OPERATOR"
    )
