import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/independent_mascon_nonzero_baseline_or_external_gravity_model_comparison_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/IndependentMASCONNonzeroBaselineOrExternalGravityModelComparison.lean")

def test_target_only_status():
    artifact = json.loads(ART.read_text())
    assert artifact["comparison_executable"] is False
    assert artifact["external_baseline_supplied"] is False
    assert artifact["empirical_gravity_result"] is False

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert all(artifact["boundary"].values())

def test_weakest_missing_object():
    artifact = json.loads(ART.read_text())
    assert artifact["weakest_missing_object"] == "INDEPENDENT_NONZERO_MASCON_BASELINE_VECTOR_OR_EXTERNAL_GRAVITY_MODEL_VECTOR"

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "independentMASCONNonzeroBaselineOrExternalGravityModelComparison_blocked" in text
    assert "independentMASCONNonzeroBaselineOrExternalGravityModelComparison_boundary" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_independent_mascon_nonzero_baseline_or_external_gravity_model_comparison.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "INDEPENDENT_MASCON_NONZERO_BASELINE_OR_EXTERNAL_GRAVITY_MODEL_COMPARISON_OK" in result.stdout
