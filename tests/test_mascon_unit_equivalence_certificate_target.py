import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/mascon_unit_equivalence_certificate_target_2026_05_30.json"

def test_mascon_unit_equivalence_certificate_target_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_unit_equivalence_certificate_target.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_UNIT_EQUIVALENCE_CERTIFICATE_TARGET_OK" in result.stdout

def test_mascon_unit_equivalence_certificate_target_missing_inputs():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    assert artifact["target"]["mascon_unit_equivalence_certificate_supplied"] is False
    assert artifact["target"]["mascon_grid_units_bound"] is False
    assert artifact["target"]["unit_conversion_law_supplied"] is False
    assert "MASCON_GRID_UNIT_DECLARATION" in artifact["weakest_missing_inputs"]

def test_mascon_unit_equivalence_certificate_target_boundary():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    boundary = artifact["boundary"]
    assert boundary["empirical_gravity_result_claimed"] is False
    assert boundary["general_relativity_failure_claimed"] is False
    assert boundary["dark_matter_replacement_claimed"] is False
    assert boundary["lambda_cdm_failure_claimed"] is False
