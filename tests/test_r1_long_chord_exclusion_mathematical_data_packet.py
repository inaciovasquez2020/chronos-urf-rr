import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "artifacts/chronos/r1_long_chord_exclusion_mathematical_data_packet_2026_05_24.json"
SCHEMA = ROOT / "artifacts/chronos/r1_r2_r3_mathematical_data_accuracy_schema_2026_05_24.json"
PROGRESSIVE = ROOT / "artifacts/chronos/r1_r2_r3_progressive_witness_packet_2026_05_24.json"

def run_checker(path):
    return subprocess.run(
        [sys.executable, "tools/check_r1_long_chord_exclusion_mathematical_data_packet.py", str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

def test_r1_long_chord_packet_checker_accepts_supplied_data():
    result = run_checker(PACKET)
    assert result.returncode == 0
    assert "R1_LONG_CHORD_DATA_PACKET_OK" in result.stdout

def test_r1_long_chord_packet_checker_rejects_actual_long_chord(tmp_path):
    data = json.loads(PACKET.read_text())
    data["objects"]["candidate_chords"] = [["v0", "v4"]]
    data["computed_quantities"]["candidate_distances"] = {"v0--v4": 4}
    data["computed_quantities"]["max_candidate_skeleton_distance"] = 4
    data["computed_quantities"]["computed_long_chords"] = [["v0", "v4"]]
    data["computed_quantities"]["computed_long_chords_absent"] = False
    bad = tmp_path / "bad_long_chord_packet.json"
    bad.write_text(json.dumps(data, indent=2))
    result = run_checker(bad)
    assert result.returncode != 0
    assert "long chord witness exists" in (result.stdout + result.stderr)

def test_r1_mathematical_data_schema_is_filled():
    data = json.loads(SCHEMA.read_text())
    r1 = data["targets"]["R1_LONG_CHORD_EXCLUSION"]
    required = data["accuracy_policy"]["minimum_verified_fields_per_target"]
    assert all(r1[field] not in (None, [], {}, "") for field in required)
    assert r1["checker_contract"] == "tools/check_r1_long_chord_exclusion_mathematical_data_packet.py"

def test_progressive_packet_marks_r1_supplied_not_proved():
    data = json.loads(PROGRESSIVE.read_text())
    r1 = data["targets"]["R1"]
    assert r1["state"] == "SUPPLIED"
    assert r1["verification_result"] == "FINITE_DATA_CHECKER_SUPPLIED_NOT_LEAN_PROOF"
    assert data["closure_ready"] is False
