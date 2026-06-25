import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools" / "verify_represents_terminal_preserves_discharge_semantics_rule_target_2026_06_24.py"
def test_represents_terminal_preserves_discharge_semantics_rule_target_verifier(): assert "REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_TARGET_2026_06_24_OK" in subprocess.run([sys.executable, str(VERIFY)], cwd=ROOT, text=True, capture_output=True, check=True).stdout
