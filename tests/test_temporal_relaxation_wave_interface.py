import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_temporal_relaxation_wave_interface_verifier():
    subprocess.run(
        ["python3", "tools/verify_temporal_relaxation_wave_interface.py"],
        cwd=ROOT,
        check=True,
    )

def test_temporal_relaxation_wave_interface_boundary_doc():
    text = (ROOT / "docs/status/TEMPORAL_RELAXATION_WAVE_INTERFACE_2026_05_18.md").read_text()
    assert "Status: `INTERFACE_ONLY`" in text
    assert "Does not prove:" in text
    assert "physical time travel" in text
    assert "unrestricted Chronos-RR" in text
    assert "any Clay problem" in text
