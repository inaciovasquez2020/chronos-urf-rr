import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_order_surface_to_rate_thick_bridge_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_order_surface_to_rate_thick_fiber_coercivity_bridge.py"],
        cwd=ROOT,
        check=True,
    )

def test_order_surface_to_rate_thick_bridge_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/order_surface_to_rate_thick_fiber_coercivity_bridge_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "CONDITIONAL_BRIDGE_CLOSED_MEASURE_FIBER_MASS_FRONTIER_OPEN"
    assert artifact["weakest_missing_lemma"] == "UniversalWeakestMissingMeasureFiberMassLemma"
    boundary = "\n".join(artifact["boundary"])
    assert "does not prove unrestricted RateThickFiberCoercivity" in boundary
    assert "does not prove unrestricted UniversalFiberEntropyGap" in boundary
    assert "does not prove P vs NP" in boundary

def test_order_surface_to_rate_thick_bridge_lean_surface_has_no_sorry():
    lean = (ROOT / "lean/Chronos/Frontier/OrderSurfaceToRateThickFiberCoercivityBridge.lean").read_text()
    assert "theorem OrderSurfaceToRateThickFiberCoercivityBridge_solved" in lean
    assert "theorem unrestricted_rate_thick_reduced_to_measure_fiber_mass_floor" in lean
    assert "def UniversalWeakestMissingMeasureFiberMassLemma" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
