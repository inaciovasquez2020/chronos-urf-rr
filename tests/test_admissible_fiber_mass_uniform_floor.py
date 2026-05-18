import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_admissible_fiber_mass_uniform_floor_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_admissible_fiber_mass_uniform_floor.py"],
        cwd=ROOT,
        check=True,
    )

def test_admissible_fiber_mass_uniform_floor_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/admissible_fiber_mass_uniform_floor_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "ADMISSIBLE_FIBER_MASS_FLOOR_CLOSED_RESTRICTED_ONLY"
    boundary = "\n".join(artifact["boundary"])
    assert "admissible restricted fiber-mass floor only" in boundary
    assert "does not prove unrestricted RateThickFiberCoercivity" in boundary
    assert "does not prove unrestricted UniversalFiberEntropyGap" in boundary
    assert "does not prove P vs NP" in boundary

def test_admissible_fiber_mass_uniform_floor_lean_surface_has_no_sorry():
    lean = (ROOT / "lean/Chronos/Frontier/AdmissibleFiberMassUniformFloor.lean").read_text()
    assert "theorem AdmissibleFiberMassUniformFloor_solved" in lean
    assert "theorem AdmissibleRateThickFiberCoercivityTarget_solved" in lean
    assert "theorem AdmissibleFiberMassData_nonempty" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
