import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/concrete_gravity_analytic_estimate_readiness_2026_05_28.json"
DOC = ROOT / "docs/status/CONCRETE_GRAVITY_ANALYTIC_ESTIMATE_READINESS_2026_05_28.md"
VERIFY = ROOT / "tools/verify_concrete_gravity_analytic_estimate_readiness.py"

def test_artifact_readiness_status():
    data = json.loads(ART.read_text())
    assert data["status"] == "ANALYTIC_ESTIMATE_READINESS_PACKAGE_ONLY_NO_ESTIMATE_PROOF"
    assert data["missing_proof"].startswith("ConcreteGravityCoerciveEstimate:")

def test_readiness_items_present():
    data = json.loads(ART.read_text())
    items = set(data["readiness_items"])
    assert "selected data class named" in items
    assert "curvature-energy norm named" in items
    assert "quasi-local collapse functional named" in items
    assert "boundary-flux error term named" in items
    assert "coercive estimate shape named" in items
    assert "missing proof isolated" in items

def test_boundary_no_gravity_overclaim():
    data = json.loads(ART.read_text())
    boundary = set(data["boundary"])
    assert "no analytic estimate proof" in boundary
    assert "no Cosmic Censorship" in boundary
    assert "no Hoop Conjecture" in boundary
    assert "no Clay problem" in boundary

def test_status_doc_has_estimate_shape_and_boundary():
    text = DOC.read_text()
    assert "QL_gate(data; S) <= C * E_grav(data) + Flux_boundary(data; S)" in text
    assert "readiness package only" in text
    assert "does not prove an analytic estimate" in text

def test_verifier_runs():
    result = subprocess.run(["python3", str(VERIFY)], cwd=ROOT, text=True, capture_output=True, check=True)
    assert "CONCRETE_GRAVITY_ANALYTIC_ESTIMATE_READINESS_OK" in result.stdout
