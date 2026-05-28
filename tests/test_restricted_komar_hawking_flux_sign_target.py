import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/restricted_komar_hawking_flux_sign_target_2026_05_28.json"
DOC = ROOT / "docs/status/RESTRICTED_KOMAR_HAWKING_FLUX_SIGN_TARGET_2026_05_28.md"
VERIFY = ROOT / "tools/verify_restricted_komar_hawking_flux_sign_target.py"

def test_status_and_target_lemma():
    data = json.loads(ART.read_text())
    assert data["status"] == "RESTRICTED_FLUX_SIGN_TARGET_ONLY_NO_SIGN_PROOF"
    assert data["target_lemma"] == "RestrictedKomarHawkingFluxSign"

def test_sign_claim_shape():
    data = json.loads(ART.read_text())
    assert "Flux_boundary(data; S) >= 0" in data["sign_claim_shape"]
    assert "Komar" in data["flux_object"]
    assert "Hawking" in data["flux_object"]

def test_missing_inputs_present():
    data = json.loads(ART.read_text())
    missing = set(data["missing_inputs"])
    assert "orientation convention for S" in missing
    assert "energy condition used for sign" in missing
    assert "surface admissibility hypothesis" in missing

def test_boundary_no_overclaim():
    data = json.loads(ART.read_text())
    boundary = set(data["boundary"])
    assert "no flux sign proof" in boundary
    assert "no restricted estimate proof" in boundary
    assert "no Cosmic Censorship" in boundary
    assert "no Hoop Conjecture" in boundary
    assert "no Clay problem" in boundary

def test_status_doc_boundary_language():
    text = DOC.read_text()
    assert "target lemma only" in text
    assert "does not prove the flux sign" in text
    assert "unrestricted Chronos-RR" in text
    assert "unrestricted H4.1/FGL" in text

def test_verifier_runs():
    result = subprocess.run(["python3", str(VERIFY)], cwd=ROOT, text=True, capture_output=True, check=True)
    assert "RESTRICTED_KOMAR_HAWKING_FLUX_SIGN_TARGET_OK" in result.stdout
