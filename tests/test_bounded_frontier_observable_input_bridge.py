from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_bounded_frontier_observable_input_bridge_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    verifier = root / "tools" / "verify_bounded_frontier_observable_input_bridge.py"
    result = subprocess.run(
        [sys.executable, str(verifier)],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "BOUNDED_FRONTIER_OBSERVABLE_INPUT_BRIDGE_OK" in result.stdout
