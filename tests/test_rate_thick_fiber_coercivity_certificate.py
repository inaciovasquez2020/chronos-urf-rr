import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_rate_thick_fiber_coercivity_certificate_verifier():
    subprocess.run(
        ["python3", "tools/verify_rate_thick_fiber_coercivity_certificate.py"],
        cwd=ROOT,
        check=True,
    )

def test_rate_thick_fiber_coercivity_certificate_lean_surface():
    lean = (ROOT / "lean/Chronos/Frontier/RateThickFiberCoercivityCertificate.lean").read_text()
    assert "def UniformRateThickFiberLowerBoundCertificate" in lean
    assert "rateThickFiberCoercivity_from_uniformLowerBoundCertificate" in lean
    assert "rateThickFiberEntropyGap_from_uniformLowerBoundCertificate" in lean
    assert "universalFiberEntropyGap_from_uniformLowerBoundCertificate" in lean
    assert "chronosRR_from_uniformLowerBoundCertificate" in lean

def test_rate_thick_fiber_coercivity_certificate_boundary():
    doc = (ROOT / "docs/status/RATE_THICK_FIBER_COERCIVITY_CERTIFICATE_2026_05_17.md").read_text()
    assert "Certificate input surface only." in doc
    assert "Does not construct:" in doc
    assert "RateThickFiberCoercivity" in doc
    assert "UniversalFiberEntropyGap" in doc
    assert "unrestricted Chronos-RR" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
