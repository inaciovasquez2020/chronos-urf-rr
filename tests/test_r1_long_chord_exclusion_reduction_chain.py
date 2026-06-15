import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/r1_long_chord_exclusion_reduction_chain_2026_06_15.json"
VERIFY = ROOT / "tools/verify_r1_long_chord_exclusion_reduction_chain.py"


def test_r1_chain_artifact_shape():
    data = json.loads(ARTIFACT.read_text())
    assert data["artifact"] == "R1_LONG_CHORD_EXCLUSION_REDUCTION_CHAIN"
    assert data["status"] == "conditional_reduction_chain"
    assert data["boundary"] == "BOUNDARY := ¬ R1_solved"
    assert {c["id"] for c in data["components"]} == {"R1a", "R1b", "R1c"}


def test_r1_chain_no_theorem_overclaim():
    text = ARTIFACT.read_text()
    forbidden = [
        "R1 solved",
        "R1 theorem solved",
        "FGL solved",
        "scientific closure achieved",
    ]
    for phrase in forbidden:
        assert phrase not in text


def test_r1_chain_verifier_passes():
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "R1_LONG_CHORD_EXCLUSION_REDUCTION_CHAIN_OK" in result.stdout
