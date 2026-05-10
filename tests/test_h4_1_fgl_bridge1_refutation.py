import json
from pathlib import Path
import subprocess


def test_h4_1_fgl_bridge1_refutation_verifier():
    subprocess.run(
        ["python3", "tools/verify_h4_1_fgl_bridge1_refutation.py"],
        check=True,
    )


def test_h4_1_fgl_bridge1_refutation_artifact_boundary():
    artifact = json.loads(Path("artifacts/chronos/h4_1_fgl_bridge1_refutation.json").read_text())
    assert artifact["status"] == "BRIDGE_1_REFUTED"
    assert "No unrestricted H4.1/FGL closure" in artifact["boundary"]
    assert "No P vs NP or Clay-problem closure" in artifact["boundary"]


def test_h4_1_fgl_bridge1_refutation_lean_surface():
    lean = Path("Chronos/Frontier/H4_1_FGL_Bridge1Refutation.lean").read_text()
    assert "admissible_to_final_carrier_domain_false" in lean
    assert "zeroArityCarrier" in lean
    assert "¬ FinalCarrierDomain zeroArityCarrier" in lean
