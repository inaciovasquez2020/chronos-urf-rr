import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/mascon_unit_equivalence_certificate_2026_05_30.json"

def test_mascon_unit_equivalence_certificate_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_unit_equivalence_certificate.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_UNIT_EQUIVALENCE_CERTIFICATE_OK" in result.stdout

def test_mascon_unit_equivalence_certificate_supplied_without_empirical_result():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    cert = artifact["certificate"]
    assert cert["mascon_unit_equivalence_certificate_supplied"] is True
    assert cert["conversion_factor"] == 1.0
    assert cert["same_physical_dimension"] is True
    assert cert["time_dependent_source_to_mascon_operator_closed"] is False
    assert artifact["boundary"]["empirical_gravity_result_claimed"] is False

def test_mascon_unit_equivalence_certificate_next_object():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    assert artifact["next_admissible_object"] == "TIME_DEPENDENT_SOURCE_TO_MASCON_OPERATOR"
