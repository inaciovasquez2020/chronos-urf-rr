import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/restricted_stationary_gravity_estimate_candidate_2026_05_28.json"
DOC = ROOT / "docs/status/RESTRICTED_STATIONARY_GRAVITY_ESTIMATE_CANDIDATE_2026_05_28.md"
VERIFY = ROOT / "tools/verify_restricted_stationary_gravity_estimate_candidate.py"

def test_candidate_status_and_shape():
    data = json.loads(ART.read_text())
    assert data["status"] == "RESTRICTED_CANDIDATE_LEMMA_ONLY_NO_GRAVITY_ESTIMATE_PROOF"
    assert data["candidate_estimate"] == "QL_gate(data; S) <= C(r, M) * (int_Sigma mu_0 dV + O(r^-3)) + Flux_infty^(0)(r)"

def test_missing_lemmas_are_named():
    data = json.loads(ART.read_text())
    missing = set(data["missing_lemmas"])
    assert "RestrictedStationarySurfaceAdmissibility" in missing
    assert "RestrictedKomarHawkingFluxSign" in missing
    assert "RestrictedAsymptoticDecayErrorBound" in missing
    assert "RestrictedQLGateMassControl" in missing

def test_boundary_no_overclaim():
    data = json.loads(ART.read_text())
    boundary = set(data["boundary"])
    assert "no restricted estimate proof" in boundary
    assert "no coercive estimate proof" in boundary
    assert "no Cosmic Censorship" in boundary
    assert "no Hoop Conjecture" in boundary
    assert "no Clay problem" in boundary

def test_status_doc_shape_test():
    text = DOC.read_text()
    assert "malformed or incorrectly oriented" in text
    assert "does not prove the restricted estimate" in text
    assert "unrestricted Chronos-RR" in text
    assert "unrestricted H4.1/FGL" in text

def test_verifier_runs():
    result = subprocess.run(["python3", str(VERIFY)], cwd=ROOT, text=True, capture_output=True, check=True)
    assert "RESTRICTED_STATIONARY_GRAVITY_ESTIMATE_CANDIDATE_OK" in result.stdout
