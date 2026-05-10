import json
from pathlib import Path
import subprocess


def test_h4_1_fgl_restricted_domain_reduction_verifier():
    subprocess.run(
        ["python3", "tools/verify_h4_1_fgl_restricted_domain_reduction.py"],
        check=True,
    )


def test_h4_1_fgl_restricted_domain_reduction_artifact_boundary():
    artifact = json.loads(Path("artifacts/chronos/h4_1_fgl_restricted_domain_reduction.json").read_text())
    assert artifact["status"] == "RESTRICTED_DOMAIN_REDUCTION_ONLY"
    assert "No unrestricted H4.1/FGL closure" in artifact["boundary"]
    assert "No P vs NP or Clay-problem closure" in artifact["boundary"]


def test_h4_1_fgl_restricted_domain_reduction_lean_surface():
    lean = Path("Chronos/Frontier/H4_1_FGL_RestrictedDomainReduction.lean").read_text()
    assert "h4_1_fgl_unrestricted_bridge1_refuted" in lean
    assert "h4_1_fgl_final_domain_reduction" in lean
    assert "h4_1_fgl_intended_domain_reduction" in lean
