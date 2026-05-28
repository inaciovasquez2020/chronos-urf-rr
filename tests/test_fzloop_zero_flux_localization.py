import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/fzloop_zero_flux_localization_2026_05_28.json"
DOC = ROOT / "docs/status/FZLOOP_ZERO_FLUX_LOCALIZATION_2026_05_28.md"
VERIFY = ROOT / "tools/verify_fzloop_zero_flux_localization.py"

def test_artifact_status_and_theorem():
    data = json.loads(ART.read_text())
    assert data["status"] == "FZLOOP_ZERO_FLUX_LOCALIZATION_PROVED_FINITE_NONNEGATIVE_MODEL_ONLY"
    assert data["toolkit_name"] == "FZloop"
    assert data["lean_theorem"] == "FZLoop.zero_flux_localization"

def test_gravity_use_is_restricted():
    data = json.loads(ART.read_text())
    assert "restricted stationary gravity estimates" in data["intended_gravity_use"]
    assert "nonnegative sectors" in data["intended_gravity_use"]

def test_boundary_no_overclaim():
    data = json.loads(ART.read_text())
    boundary = set(data["boundary"])
    assert "no Komar sign proof" in boundary
    assert "no Hawking mass theorem" in boundary
    assert "no restricted estimate proof" in boundary
    assert "no Cosmic Censorship" in boundary
    assert "no Clay problem" in boundary

def test_status_doc_boundary_language():
    text = DOC.read_text()
    assert "finite nonnegative model lemma" in text
    assert "does not prove a Komar sign theorem" in text
    assert "unrestricted Chronos-RR" in text
    assert "unrestricted H4.1/FGL" in text

def test_verifier_runs():
    result = subprocess.run(["python3", str(VERIFY)], cwd=ROOT, text=True, capture_output=True, check=True)
    assert "FZLOOP_ZERO_FLUX_LOCALIZATION_OK" in result.stdout
