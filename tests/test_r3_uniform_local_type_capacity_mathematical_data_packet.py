import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "artifacts/chronos/r3_uniform_local_type_capacity_mathematical_data_packet_2026_05_24.json"
SCHEMA = ROOT / "artifacts/chronos/r1_r2_r3_mathematical_data_accuracy_schema_2026_05_24.json"
PROGRESSIVE = ROOT / "artifacts/chronos/r1_r2_r3_progressive_witness_packet_2026_05_24.json"

def run_checker(path):
    return subprocess.run(
        [sys.executable, "tools/check_r3_uniform_local_type_capacity_mathematical_data_packet.py", str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

def test_r3_packet_checker_accepts_supplied_data():
    result = run_checker(PACKET)
    assert result.returncode == 0
    assert "R3_UNIFORM_LOCAL_TYPE_CAPACITY_PACKET_OK" in result.stdout

def test_r3_packet_checker_rejects_capacity_violation(tmp_path):
    data = json.loads(PACKET.read_text())
    data["objects"]["capacity_bound"] = 1
    data["computed_quantities"]["capacity_bound"] = 1
    data["computed_quantities"]["uniform_capacity_bound_satisfied"] = False
    data["computed_quantities"]["computed_capacity_instance_present"] = False
    bad = tmp_path / "bad_r3_packet.json"
    bad.write_text(json.dumps(data, indent=2))
    result = run_checker(bad)
    assert result.returncode != 0
    assert "uniform local-type capacity bound violated" in (result.stdout + result.stderr)

def test_r3_mathematical_data_schema_is_filled():
    data = json.loads(SCHEMA.read_text())
    r3 = data["targets"]["R3_UNIFORM_LOCAL_TYPE_CAPACITY"]
    required = data["accuracy_policy"]["minimum_verified_fields_per_target"]
    assert all(r3[field] not in (None, [], {}, "") for field in required)
    assert r3["checker_contract"] == "tools/check_r3_uniform_local_type_capacity_mathematical_data_packet.py"

def test_progressive_packet_marks_r3_supplied_not_proved():
    data = json.loads(PROGRESSIVE.read_text())
    r3 = data["targets"]["R3"]
    assert r3["state"] == "SUPPLIED"
    assert r3["verification_result"] == "FINITE_DATA_CHECKER_SUPPLIED_NOT_LEAN_PROOF"
    assert data["closure_ready"] is False
