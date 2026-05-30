import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/mascon_model_comparison_interpretation_boundary_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/MASCONModelComparisonInterpretationBoundary.lean")

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert artifact["external_baseline_comparison"] is False
    assert artifact["empirical_gravity_result"] is False
    assert all(artifact["boundary"].values())

def test_forbidden_interpretation():
    artifact = json.loads(ART.read_text())
    assert "does not compare against GR" in artifact["forbidden_interpretation"]
    assert "does not falsify GR" in artifact["forbidden_interpretation"]

def test_lean_theorem_present():
    text = LEAN.read_text()
    assert "masconModelComparisonInterpretationBoundary_boundary" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_model_comparison_interpretation_boundary.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_MODEL_COMPARISON_INTERPRETATION_BOUNDARY_OK" in result.stdout
