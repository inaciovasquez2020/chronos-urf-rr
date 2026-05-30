import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/mascon_grid_unit_declaration_2026_05_30.json"

def test_mascon_grid_unit_declaration_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_grid_unit_declaration.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_GRID_UNIT_DECLARATION_OK" in result.stdout

def test_mascon_grid_unit_declaration_records_units():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    decl = artifact["declaration"]
    assert decl["physical_grid_units_bound"] is True
    assert decl["mascon_grid_units_declared"] is True
    assert decl["source_grid_to_mascon_grid_conversion_law_supplied"] is False

def test_mascon_grid_unit_declaration_boundary():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    boundary = artifact["boundary"]
    assert boundary["empirical_gravity_result_claimed"] is False
    assert boundary["general_relativity_failure_claimed"] is False
    assert boundary["dark_matter_replacement_claimed"] is False
    assert boundary["lambda_cdm_failure_claimed"] is False
