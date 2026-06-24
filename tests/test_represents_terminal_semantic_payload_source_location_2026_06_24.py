import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools" / "verify_represents_terminal_semantic_payload_source_location_2026_06_24.py"

def test_represents_terminal_semantic_payload_source_location_verifier():
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_LOCATION_2026_06_24_OK" in result.stdout
