from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_measure_fiber_mass_package.py"],
        cwd=ROOT,
        check=True,
    )

def test_artifact_status_and_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/measure_fiber_mass_package_2026_05_18.json").read_text()
    )
    assert artifact["target"] == "MeasureFiberMassPackage"
    assert artifact["status"] == "MEASURE_FIBER_MASS_PACKAGE_FINITE_SUPPORT_PUSHFORWARD_CLOSED_FRONTIER_OPEN"
    boundary = "\n".join(artifact["boundary"])
    assert "finite-support pushforward case only" in boundary
    assert "restricted-domain RateThickFiberCoercivity bridge only" in boundary
    assert "unrestricted measure case remains FRONTIER_OPEN" in boundary
    assert "no unrestricted UniversalFiberEntropyGap" in boundary
    assert "no Clay-problem closure" in boundary

def test_lean_surface_contains_requested_objects():
    text = (ROOT / "lean/Chronos/Frontier/MeasureFiberMassPackage.lean").read_text()
    assert "structure MeasureFiberMassPackage" in text
    assert "structure MeasureFiberMassUniformFloor" in text
    assert "finite_support_pushforward_case_from_finite_positive" in text
    assert "unrestricted_measure_fiber_mass_case_frontier_open" in text
    assert "RestrictedRateThickFiberCoercivity" in text
    assert "restricted_rate_thick_fiber_coercivity_from_finite_admissible_floor" in text
    assert "admit" not in text
    assert "sorry" not in text
    assert "axiom" not in text
