import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_entropy_dissipation_certificate_verifier():
    subprocess.run(
        ["python3", "tools/verify_restricted_entropy_dissipation_certificate.py"],
        cwd=ROOT,
        check=True,
    )

def test_restricted_entropy_dissipation_certificate_boundary_doc():
    text = (ROOT / "docs/status/RESTRICTED_ENTROPY_DISSIPATION_CERTIFICATE_2026_05_18.md").read_text()
    assert "Status: `INTERFACE_BRIDGE_ONLY`" in text
    assert "same-functional Lyapunov route" in text
    assert "Does not prove:" in text
    assert "entropy production" in text
    assert "construction of an admissible domain" in text
    assert "unrestricted Chronos-RR" in text
    assert "any Clay problem" in text
