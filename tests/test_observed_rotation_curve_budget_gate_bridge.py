from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_observed_rotation_curve_budget_gate_bridge_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_observed_rotation_curve_budget_gate_bridge.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "OBSERVED_ROTATION_CURVE_BUDGET_GATE_BRIDGE_OK" in result.stdout

def test_observed_rotation_curve_budget_gate_bridge_lean_surface_tokens():
    text = (ROOT / "lean/Chronos/Frontier/ObservedRotationCurveBudgetGateBridge.lean").read_text()
    assert "physicalGDMBudget_partitioned_certificate_from_observed_rotation_curve" in text
    assert "physicalGDM_observed_rotation_curve_feeds_gate" in text
    assert "hReading" in text
    assert "hPartition" in text
