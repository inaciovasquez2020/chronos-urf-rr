import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_dissipation_to_rate_thick_coercivity_surface_verifier():
    subprocess.run(
        ["python3", "tools/verify_restricted_dissipation_to_rate_thick_coercivity_surface.py"],
        cwd=ROOT,
        check=True,
    )

def test_restricted_dissipation_to_rate_thick_coercivity_surface_boundary_doc():
    text = (ROOT / "docs/status/RESTRICTED_DISSIPATION_TO_RATE_THICK_COERCIVITY_SURFACE_2026_05_18.md").read_text()
    assert "Status: `INTERFACE_BRIDGE_ONLY`" in text
    assert "restricted admissible-dissipation surface" in text
    assert "restricted rate-thick coercivity surface" in text
    assert "Does not prove:" in text
    assert "unrestricted rate-thick coercivity" in text
    assert "unrestricted Chronos-RR" in text
    assert "any Clay problem" in text
