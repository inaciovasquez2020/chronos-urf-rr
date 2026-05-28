import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/concrete_gravity_estimate_target_2026_05_28.json"
DOC = ROOT / "docs/status/CONCRETE_GRAVITY_ESTIMATE_TARGET_2026_05_28.md"
VERIFY = ROOT / "tools/verify_concrete_gravity_estimate_target.py"

def test_artifact_status_and_missing_lemma():
    data = json.loads(ART.read_text())
    assert data["status"] == "CONCRETE_GRAVITY_ESTIMATE_TARGET_ONLY_NO_ANALYTIC_PROOF"
    assert data["missing_analytic_lemma"].startswith("ConcreteGravityCoerciveEstimate")

def test_boundary_no_gravity_overclaim():
    data = json.loads(ART.read_text())
    boundary = set(data["boundary"])
    assert "no Cosmic Censorship" in boundary
    assert "no Hoop Conjecture" in boundary
    assert "no quantum gravity" in boundary
    assert "no Clay problem" in boundary

def test_status_doc_boundary_language():
    text = DOC.read_text()
    assert "target registry only" in text
    assert "does not prove an analytic estimate" in text
    assert "unrestricted Chronos-RR" in text
    assert "unrestricted H4.1/FGL" in text

def test_verifier_runs():
    result = subprocess.run(["python3", str(VERIFY)], cwd=ROOT, text=True, capture_output=True, check=True)
    assert "CONCRETE_GRAVITY_ESTIMATE_TARGET_OK" in result.stdout
