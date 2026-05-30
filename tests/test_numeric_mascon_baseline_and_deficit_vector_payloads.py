import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/numeric_mascon_baseline_and_deficit_vector_payloads_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/NumericMASCONBaselineAndDeficitVectorPayloads.lean")

def test_artifact_metadata():
    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "LOCAL_NUMERIC_PAYLOADS_GENERATED_NOT_COMMITTED"
    assert artifact["source_variable"] == "lwe_thickness"
    assert artifact["shape"] == [255, 360, 720]
    assert artifact["vector_length"] == 66096000

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert artifact["boundary"]["no_model_comparison_execution"] is True
    assert artifact["boundary"]["no_empirical_gravity_result"] is True
    assert all(artifact["boundary"].values())

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "numericMASCONBaselineAndDeficitVectorPayloads_shape" in text
    assert "numericMASCONBaselineAndDeficitVectorPayloads_boundary" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_numeric_mascon_baseline_and_deficit_vector_payloads.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "NUMERIC_MASCON_BASELINE_AND_DEFICIT_VECTOR_PAYLOADS_OK" in result.stdout
