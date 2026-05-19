import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_admissible_dissipation_surface_verifier():
    subprocess.run(
        ["python3", "tools/verify_restricted_admissible_dissipation_surface.py"],
        cwd=ROOT,
        check=True,
    )

def test_restricted_admissible_dissipation_surface_boundary_doc():
    text = (ROOT / "docs/status/RESTRICTED_ADMISSIBLE_DISSIPATION_SURFACE_2026_05_18.md").read_text()
    assert "Status: `INTERFACE_BRIDGE_ONLY`" in text
    assert "restricted entropy-dissipation certificate" in text
    assert "Does not prove:" in text
    assert "existence of admissible dissipation certificates" in text
    assert "construction of an admissible domain" in text
    assert "unrestricted Chronos-RR" in text
    assert "any Clay problem" in text
