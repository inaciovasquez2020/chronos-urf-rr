import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_finite_positive_fiber_mass_no_warning_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_finite_positive_fiber_mass_uniform_floor_no_warning.py"],
        cwd=ROOT,
        check=True,
    )

def test_finite_positive_fiber_mass_no_warning_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/finite_positive_fiber_mass_uniform_floor_no_warning_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "FINITE_POSITIVE_FIBER_MASS_UNIFORM_FLOOR_WARNING_CLEANUP_CLOSED"
    boundary = "\n".join(artifact["boundary"])
    assert "warning cleanup only" in boundary
    assert "does not prove unrestricted FiberMassUniformFloor for arbitrary FiberMassData" in boundary
    assert "does not prove P vs NP" in boundary

def test_finite_positive_fiber_mass_no_warning_binder_removed():
    lean = (ROOT / "lean/Chronos/Frontier/FinitePositiveFiberMassUniformFloor.lean").read_text()
    start = lean.index("def FinitePositiveFiberMassUniformFloorTheorem : Prop :=")
    end = lean.index("theorem FinitePositiveFiberMassUniformFloorTheorem_solved")
    wrapper = lean[start:end]
    assert "(hN : 0 < N)" not in wrapper
    assert "(_ : 0 < N)" in wrapper
