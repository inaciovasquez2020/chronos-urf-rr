import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/source_grid_to_mascon_grid_unit_conversion_law_2026_05_30.json"

def test_source_grid_to_mascon_grid_unit_conversion_law_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_source_grid_to_mascon_grid_unit_conversion_law.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "SOURCE_GRID_TO_MASCON_GRID_UNIT_CONVERSION_LAW_OK" in result.stdout

def test_source_grid_to_mascon_grid_unit_conversion_law_records_identity_conversion():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    law = artifact["conversion_law"]
    assert law["conversion_law_supplied"] is True
    assert law["conversion_factor"] == 1.0
    assert law["dimension_preserving"] is True
    assert law["source_to_mascon_numeric_identity_after_unit_declaration"] is True

def test_source_grid_to_mascon_grid_unit_conversion_law_preserves_missing_certificate():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    law = artifact["conversion_law"]
    assert law["authentic_comparison_metric_supplied"] is False
    assert law["mascon_unit_equivalence_certificate_supplied"] is False
    assert law["time_dependent_source_to_mascon_operator_closed"] is False

def test_source_grid_to_mascon_grid_unit_conversion_law_boundary():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    boundary = artifact["boundary"]
    assert boundary["empirical_gravity_result_claimed"] is False
    assert boundary["general_relativity_failure_claimed"] is False
    assert boundary["dark_matter_replacement_claimed"] is False
    assert boundary["lambda_cdm_failure_claimed"] is False
