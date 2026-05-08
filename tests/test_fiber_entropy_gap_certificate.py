import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/fiber_entropy_gap_certificate.json"

def test_fiber_entropy_gap_certificate_boundary():
    data = json.loads(ART.read_text())
    assert data["status"] == "CERTIFICATE_INTERFACE_ONLY"
    assert data["theorem_closure"] is False
    assert data["chronos_rr_closure"] is False
    assert data["h41_fgl_closure"] is False
    assert data["p_vs_np_closure"] is False

def test_fiber_entropy_gap_certificate_conditional_result():
    data = json.loads(ART.read_text())
    assert data["proved_conditional"] == [
        "CertificateFiberEntropyGap implies CertificateRankImageBound",
    ]
    assert data["missing_universal_object"] == "UniversalFiberEntropyGap"

def test_fiber_entropy_gap_certificate_verifier():
    subprocess.run(
        ["python3", "tools/verify_fiber_entropy_gap_certificate.py"],
        cwd=ROOT,
        check=True,
    )
