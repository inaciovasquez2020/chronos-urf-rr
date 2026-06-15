import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN_FILE = ROOT / "lean/Chronos/Frontier/R1WtrivSupportBridge.lean"
VERIFY = ROOT / "tools/verify_r1_wtriv_support_bridge_lean.py"


def test_r1_wtriv_bridge_verifier_passes():
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "R1_WTRIV_SUPPORT_BRIDGE_LEAN_OK" in result.stdout


def test_r1_wtriv_bridge_lean_declares_named_route():
    text = LEAN_FILE.read_text()
    assert "R1WtrivSupportGenerationBridge_from_semantic_inputs" in text
    assert "R1_exactWtriv_support_statement_from_R1a_R1b_R1c_bridge" in text
    assert "R1LongChordExclusionTheorem D" in text


def test_r1_wtriv_bridge_has_no_forbidden_proof_debt_markers():
    text = LEAN_FILE.read_text()
    for forbidden in ["axiom ", "opaque ", "sorry", "admit"]:
        assert forbidden not in text
