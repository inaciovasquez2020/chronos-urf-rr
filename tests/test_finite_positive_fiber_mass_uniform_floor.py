import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_finite_positive_fiber_mass_uniform_floor_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_finite_positive_fiber_mass_uniform_floor.py"],
        cwd=ROOT,
        check=True,
    )

def test_finite_positive_fiber_mass_uniform_floor_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/finite_positive_fiber_mass_uniform_floor_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "FINITE_POSITIVE_FIBER_MASS_UNIFORM_FLOOR_CLOSED"
    boundary = "\n".join(artifact["boundary"])
    assert "finite fiber-mass compactness theorem only" in boundary
    assert "does not prove unrestricted FiberMassUniformFloor for arbitrary FiberMassData" in boundary
    assert "does not prove P vs NP" in boundary

def test_finite_positive_fiber_mass_uniform_floor_lean_surface_has_no_sorry_axiom():
    lean = (ROOT / "lean/Chronos/Frontier/FinitePositiveFiberMassUniformFloor.lean").read_text()
    assert "theorem finite_positive_fiber_mass_uniform_floor" in lean
    assert "theorem FinitePositiveFiberMassUniformFloorTheorem_solved" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
    assert "axiom" not in lean
