import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_terminal_anti_branch_negative_packet.py"

def test_terminal_anti_branch_negative_packet_verifies():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    assert "TERMINAL_ANTI_BRANCH_NEGATIVE_PACKET_OK" in result.stdout
    assert '"decision": "PASS"' in result.stdout
    assert '"terminal_status": "TERMINAL_BRANCH_CLOSED_NEGATIVE_RESULT"' in result.stdout
