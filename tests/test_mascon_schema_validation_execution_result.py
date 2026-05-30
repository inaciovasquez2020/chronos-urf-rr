import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/mascon_schema_validation_execution_result_2026_05_29.json")
DOC = Path("docs/status/MASCON_SCHEMA_VALIDATION_EXECUTION_RESULT_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/MASCONSchemaValidationExecutionResult.lean")

def test_mascon_schema_validation_artifact():
    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "MASCON_SCHEMA_VALIDATION_EXECUTED"
    assert artifact["schema_validation_passed"] is True
    assert artifact["matches_authenticated_digest_manifest"] is True
    assert artifact["required_dimensions_present"] is True
    assert artifact["required_coordinate_variables_present"] is True
    assert artifact["dimension_count"] >= 3
    assert artifact["variable_count"] >= 4
    assert artifact["grid_variable_count"] > 0
    assert artifact["time_dependent_grid_variable_count"] > 0
    assert artifact["next_admissible_object"] == "MASCON_MODEL_COMPARISON_EXECUTION_TARGET"

def test_mascon_schema_validation_required_names():
    artifact = json.loads(ART.read_text())
    for name in ["time", "lat", "lon"]:
        assert name in artifact["dimensions"]
        assert name in artifact["variables"]

def test_mascon_schema_validation_doc_boundary():
    text = DOC.read_text()
    assert "Status: `MASCON_SCHEMA_VALIDATION_EXECUTED`" in text
    assert "This is schema validation only." in text
    assert "MASCON_MODEL_COMPARISON_EXECUTION_TARGET" in text

def test_mascon_schema_validation_lean_boundary():
    text = LEAN.read_text()
    assert "MASCONSchemaValidationExecutionResult" in text
    assert "mascon_schema_validation_executed" in text
    assert "mascon_schema_validation_passed" in text
    assert "mascon_schema_validation_payload_not_committed" in text

def test_mascon_schema_validation_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_schema_validation_execution_result.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_SCHEMA_VALIDATION_EXECUTION_RESULT_OK" in result.stdout
