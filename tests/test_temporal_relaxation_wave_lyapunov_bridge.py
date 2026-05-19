import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_temporal_relaxation_wave_lyapunov_bridge_verifier():
    subprocess.run(
        ["python3", "tools/verify_temporal_relaxation_wave_lyapunov_bridge.py"],
        cwd=ROOT,
        check=True,
    )

def test_temporal_relaxation_wave_lyapunov_bridge_boundary_doc():
    text = (ROOT / "docs/status/TEMPORAL_RELAXATION_WAVE_LYAPUNOV_BRIDGE_2026_05_18.md").read_text()
    assert "Status: `INTERFACE_BRIDGE_ONLY`" in text
    assert "Does not prove:" in text
    assert "existence of temporal relaxation waves" in text
    assert "unrestricted Chronos-RR" in text
    assert "any Clay problem" in text
