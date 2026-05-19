import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_lyapunov_decay_energy_control_verifier():
    subprocess.run(
        ["python3", "tools/verify_lyapunov_decay_energy_control.py"],
        cwd=ROOT,
        check=True,
    )

def test_lyapunov_decay_energy_control_boundary_doc():
    text = (ROOT / "docs/status/LYAPUNOV_DECAY_ENERGY_CONTROL_2026_05_18.md").read_text()
    assert "Status: `INTERFACE_BRIDGE_ONLY`" in text
    assert "same-functional entropy-control bridge" in text
    assert "Does not prove:" in text
    assert "entropy production" in text
    assert "entropy monotonicity for arbitrary entropy functions" in text
    assert "unrestricted Chronos-RR" in text
    assert "any Clay problem" in text
