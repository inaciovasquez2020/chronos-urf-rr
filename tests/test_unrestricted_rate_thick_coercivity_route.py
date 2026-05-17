import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_unrestricted_rate_thick_coercivity_route_verifier():
    subprocess.run(
        ["python3", "tools/verify_unrestricted_rate_thick_coercivity_route.py"],
        cwd=ROOT,
        check=True,
    )

def test_unrestricted_rate_thick_coercivity_route_lean_surface():
    lean = (ROOT / "lean/Chronos/Frontier/UnrestrictedRateThickCoercivityRoute.lean").read_text()
    assert "WeakestAnalyticInvariant lam ↔ RateThickFiberCoercivity lam" in lean
    assert "RateThickFiberEntropyGap lam" in lean
    assert "UniversalFiberEntropyGap lam" in lean
    assert "UniversalFiberEntropyGapToChronosRR lam" in lean
    assert "full_conditional_route_to_chronosRR" in lean

def test_unrestricted_rate_thick_coercivity_route_boundary():
    doc = (ROOT / "docs/status/UNRESTRICTED_RATE_THICK_COERCIVITY_ROUTE_2026_05_17.md").read_text()
    assert "Conditional route only." in doc
    assert "unrestricted RateThickFiberCoercivity" in doc
    assert "unrestricted UniversalFiberEntropyGap" in doc
    assert "unrestricted Chronos-RR" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
