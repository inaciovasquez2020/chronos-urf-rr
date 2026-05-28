import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/gdm_gravity_dark_matter_deficit_model_2026_05_28.json"
DOC = ROOT / "docs/status/GDM_GRAVITY_DARK_MATTER_DEFICIT_MODEL_2026_05_28.md"
VERIFY = ROOT / "tools/verify_gdm_gravity_dark_matter_deficit_model.py"

def test_artifact_status_and_identity():
    data = json.loads(ART.read_text())
    assert data["status"] == "GDM_DEFICIT_ACCOUNTING_MODEL_PROVED_FINITE_NONNEGATIVE_ONLY"
    assert data["toolkit_name"] == "GDM"
    assert data["core_identity"] == "effectiveMass = baryonicMass + geometricDeficitMass"

def test_proved_theorems_present():
    data = json.loads(ART.read_text())
    theorems = set(data["proved_theorems"])
    assert "GDM.baryonic_le_effective" in theorems
    assert "GDM.zero_deficit_effective_eq_baryonic" in theorems
    assert "GDM.positive_deficit_effective_gt_baryonic" in theorems
    assert "GDM.effective_eq_baryonic_implies_zero_deficit" in theorems

def test_boundary_no_dark_matter_overclaim():
    data = json.loads(ART.read_text())
    boundary = set(data["boundary"])
    assert "no observational evidence" in boundary
    assert "no galaxy rotation curve fit" in boundary
    assert "no lensing fit" in boundary
    assert "no dark matter replacement" in boundary
    assert "no Lambda-CDM refutation" in boundary
    assert "no Clay problem" in boundary

def test_status_doc_boundary_language():
    text = DOC.read_text()
    assert "finite nonnegative accounting model" in text
    assert "does not provide observational evidence" in text
    assert "dark matter replacement" in text
    assert "unrestricted Chronos-RR" in text
    assert "unrestricted H4.1/FGL" in text

def test_verifier_runs():
    result = subprocess.run(["python3", str(VERIFY)], cwd=ROOT, text=True, capture_output=True, check=True)
    assert "GDM_GRAVITY_DARK_MATTER_DEFICIT_MODEL_OK" in result.stdout
