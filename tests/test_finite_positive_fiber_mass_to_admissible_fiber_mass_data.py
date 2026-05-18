from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_finite_positive_fiber_mass_to_admissible_fiber_mass_data.py"],
        cwd=ROOT,
        check=True,
    )

def test_artifact_status_and_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/finite_positive_fiber_mass_to_admissible_fiber_mass_data_2026_05_18.json").read_text()
    )
    assert artifact["target"] == "FinitePositiveFiberMassToAdmissibleFiberMassData"
    assert artifact["status"] == "FINITE_POSITIVE_FIBER_MASS_TO_ADMISSIBLE_FIBER_MASS_DATA_CLOSED"
    boundary = "\n".join(artifact["boundary"])
    assert "admissible payload projection only" in boundary
    assert "no redeclaration of AdmissibleFiberMassData" in boundary
    assert "no unrestricted UniversalFiberEntropyGap" in boundary
    assert "no Clay-problem closure" in boundary

def test_lean_surface_uses_existing_admissible_data_without_redeclaration():
    text = (ROOT / "lean/Chronos/Frontier/FinitePositiveFiberMassToAdmissibleFiberMassData.lean").read_text()
    assert "extends AdmissibleFiberMassData" in text
    assert "D.toAdmissibleFiberMassData" in text
    assert "preserves_epsilon" in text
    assert "preserves_floor" in text
    assert "structure AdmissibleFiberMassData" not in text
    assert "Classical.choice" not in text
    assert "List.foldr" not in text
    assert "admit" not in text
    assert "sorry" not in text
