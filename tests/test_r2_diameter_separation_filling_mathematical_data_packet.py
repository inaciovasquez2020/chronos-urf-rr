import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "artifacts/chronos/r2_diameter_separation_filling_mathematical_data_packet_2026_05_24.json"
SCHEMA = ROOT / "artifacts/chronos/r1_r2_r3_mathematical_data_accuracy_schema_2026_05_24.json"
PROGRESSIVE = ROOT / "artifacts/chronos/r1_r2_r3_progressive_witness_packet_2026_05_24.json"

def run_checker(path):
    return subprocess.run(
        [sys.executable, "tools/check_r2_diameter_separation_filling_mathematical_data_packet.py", str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

def test_r2_packet_checker_accepts_supplied_data():
    result = run_checker(PACKET)
    assert result.returncode == 0
    assert "R2_DIAMETER_SEPARATION_FILLING_PACKET_OK" in result.stdout

def test_r2_packet_checker_rejects_missing_obstruction_by_diameter(tmp_path):
    data = json.loads(PACKET.read_text())
    data["objects"]["diameter_bound"] = 4
    data["computed_quantities"]["diameter_bound_satisfied"] = False
    data["computed_quantities"]["computed_obstruction_present"] = False
    bad = tmp_path / "bad_r2_packet.json"
    bad.write_text(json.dumps(data, indent=2))
    result = run_checker(bad)
    assert result.returncode != 0
    assert "computed obstruction is absent" in (result.stdout + result.stderr)

def test_r2_mathematical_data_schema_is_filled():
    data = json.loads(SCHEMA.read_text())
    r2 = data["targets"]["R2_DIAMETER_SEPARATION_FILLING_OBSTRUCTION"]
    required = data["accuracy_policy"]["minimum_verified_fields_per_target"]
    assert all(r2[field] not in (None, [], {}, "") for field in required)
    assert r2["checker_contract"] == "tools/check_r2_diameter_separation_filling_mathematical_data_packet.py"

def test_progressive_packet_marks_r2_supplied_not_proved():
    data = json.loads(PROGRESSIVE.read_text())
    r2 = data["targets"]["R2"]
    assert r2["state"] == "SUPPLIED"
    assert r2["verification_result"] == "FINITE_DATA_CHECKER_SUPPLIED_NOT_LEAN_PROOF"
    assert data["closure_ready"] is False
