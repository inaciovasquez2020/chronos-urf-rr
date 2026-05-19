import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_rate_thick_to_recovery_route_surfaces_verifier():
    subprocess.run(
        ["python3", "tools/verify_restricted_rate_thick_to_recovery_route_surfaces.py"],
        cwd=ROOT,
        check=True,
    )

def test_restricted_rate_thick_to_recovery_route_surfaces_boundary_doc():
    text = (ROOT / "docs/status/RESTRICTED_RATE_THICK_TO_RECOVERY_ROUTE_SURFACES_2026_05_18.md").read_text()
    assert "Status: `INTERFACE_BRIDGE_ONLY`" in text
    assert "restricted UniversalFiberEntropyGap route" in text
    assert "restricted Chronos-RR recovery bridge" in text
    assert "restricted H4.1/FGL recovery bridge" in text
    assert "Does not prove:" in text
    assert "unrestricted Chronos-RR" in text
    assert "unrestricted H4.1/FGL" in text
    assert "any Clay problem" in text
