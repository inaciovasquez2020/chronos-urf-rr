import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_chronos_survival_protocol_doc_exists():
    p = ROOT / "docs/status/CHRONOS_SURVIVAL_PROTOCOL.md"
    assert p.exists()
    text = p.read_text()
    assert "Status: Repository-governance protocol" in text
    assert "It does not claim that every broader URF or complexity-theoretic theorem is solved." in text
    assert "Do not expand Chronos merely by adding new terminology." in text

def test_chronos_survival_protocol_verifier_runs():
    result = subprocess.run(
        [sys.executable, "tools/verify_chronos_survival_protocol.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr + result.stdout
