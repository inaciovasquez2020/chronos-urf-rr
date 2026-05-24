import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_r1_r2_r3_isolated_targets_conditional_closure_verifier():
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_r2_r3_isolated_targets_conditional_closure.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "R1_R2_R3_ISOLATED_TARGETS_CONDITIONAL_CLOSURE_OK" in result.stdout

def test_long_chord_finite_checker_accepts_absence_packet(tmp_path):
    packet = {
        "status": "FINITE_LONG_CHORD_WITNESS_PACKET",
        "vertices": ["a", "b", "c"],
        "edges": [["a", "b"], ["b", "c"]],
        "diameter_bound": 2,
        "long_chord_threshold": 3,
        "claimed_long_chords_absent": True,
        "declared_long_chords": []
    }
    path = tmp_path / "packet.json"
    path.write_text(json.dumps(packet))
    result = subprocess.run(
        [sys.executable, "tools/check_long_chord_witness_obstruction.py", str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "LONG_CHORD_WITNESS_CHECK_OK" in result.stdout

def test_long_chord_finite_checker_rejects_declared_long_chord(tmp_path):
    packet = {
        "status": "FINITE_LONG_CHORD_WITNESS_PACKET",
        "vertices": ["a", "b", "c"],
        "edges": [["a", "b"], ["b", "c"]],
        "diameter_bound": 2,
        "long_chord_threshold": 3,
        "claimed_long_chords_absent": True,
        "declared_long_chords": [["a", "c"]]
    }
    path = tmp_path / "bad_packet.json"
    path.write_text(json.dumps(packet))
    result = subprocess.run(
        [sys.executable, "tools/check_long_chord_witness_obstruction.py", str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "LONG_CHORD_WITNESS_CHECK_FAILED" in result.stderr or "LONG_CHORD_WITNESS_CHECK_FAILED" in result.stdout
