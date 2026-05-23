import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_concrete_constraint_compatibility_certificate_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_concrete_constraint_compatibility_certificate.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "CONCRETE_CONSTRAINT_COMPATIBILITY_CERTIFICATE_ONLY_NO_ANALYTIC_ESTIMATE_PROOF" in result.stdout

def test_concrete_constraint_compatibility_certificate_artifact_boundaries():
    data = json.loads((ROOT / "artifacts/chronos/concrete_constraint_compatibility_certificate_2026_05_23.json").read_text())
    assert data["next_admissible_object"] == "ConcreteMatterCouplingCompatibilityCertificate"
    assert data["certified_gates"]["hamiltonian_constraint_compatible"] is True
    assert data["certified_gates"]["momentum_constraint_compatible"] is True
    assert "P vs NP" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
