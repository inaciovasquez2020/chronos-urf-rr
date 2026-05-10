import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_h4_1_fgl_selected_domain_restriction_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_h4_1_fgl_selected_domain_restriction.py"],
        cwd=ROOT,
        check=True,
    )

def test_h4_1_fgl_selected_domain_restriction_artifact_boundary():
    data = json.loads(
        (ROOT / "artifacts/chronos/h4_1_fgl_selected_domain_restriction.json").read_text()
    )
    assert data["status"] == "ARBITRARY_DOMAIN_REFUTED_SELECTED_DOMAIN_RESTRICTED"
    assert data["restricted_domain"] == "H4_1_FGL_SelectedTheoremDomain"
    assert "arbitrary semantic final carriers all admit separating observables" in data["refutes"]
    assert "separating observable existence for arbitrary semantic final carriers" in data["does_not_claim"]
    assert "P vs NP closure" in data["does_not_claim"]
