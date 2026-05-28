import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/concrete_gravity_coercive_estimate_proof_obligation_2026_05_28.json"
DOC = ROOT / "docs/status/CONCRETE_GRAVITY_COERCIVE_ESTIMATE_PROOF_OBLIGATION_2026_05_28.md"
VERIFY = ROOT / "tools/verify_concrete_gravity_coercive_estimate_proof_obligation.py"

def test_artifact_status_and_shape():
    data = json.loads(ART.read_text())
    assert data["status"] == "PROOF_OBLIGATION_ONLY_NO_COERCIVE_ESTIMATE_PROOF"
    assert data["estimate_shape"] == "QL_gate(data; S) <= C * E_grav(data) + Flux_boundary(data; S)"

def test_named_objects_present():
    data = json.loads(ART.read_text())
    assert data["curvature_energy_norm"] == "E_grav(data)"
    assert data["quasi_local_collapse_functional"] == "QL_gate(data; S)"
    assert data["boundary_flux_error"] == "Flux_boundary(data; S)"

def test_boundary_no_overclaim():
    data = json.loads(ART.read_text())
    boundary = set(data["boundary"])
    assert "no coercive estimate proof" in boundary
    assert "no analytic estimate proof" in boundary
    assert "no Cosmic Censorship" in boundary
    assert "no Hoop Conjecture" in boundary
    assert "no Clay problem" in boundary

def test_status_doc_boundary_language():
    text = DOC.read_text()
    assert "proof-obligation surface only" in text
    assert "does not prove the coercive estimate" in text
    assert "unrestricted Chronos-RR" in text
    assert "unrestricted H4.1/FGL" in text

def test_verifier_runs():
    result = subprocess.run(["python3", str(VERIFY)], cwd=ROOT, text=True, capture_output=True, check=True)
    assert "CONCRETE_GRAVITY_COERCIVE_ESTIMATE_PROOF_OBLIGATION_OK" in result.stdout
