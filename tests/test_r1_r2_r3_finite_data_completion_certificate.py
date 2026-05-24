import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "artifacts/chronos/r1_r2_r3_finite_data_completion_certificate_2026_05_24.json"
SCHEMA = ROOT / "artifacts/chronos/r1_r2_r3_mathematical_data_accuracy_schema_2026_05_24.json"
PROGRESSIVE = ROOT / "artifacts/chronos/r1_r2_r3_progressive_witness_packet_2026_05_24.json"

def test_finite_data_completion_certificate_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_r2_r3_finite_data_completion_certificate.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "R1_R2_R3_FINITE_DATA_COMPLETION_CERTIFICATE_OK" in result.stdout

def test_schema_structural_completeness_is_30_of_30():
    data = json.loads(SCHEMA.read_text())
    required = data["accuracy_policy"]["minimum_verified_fields_per_target"]
    filled = sum(
        1
        for target in data["targets"].values()
        for field in required
        if target[field] not in (None, [], {}, "")
    )
    total = len(data["targets"]) * len(required)
    assert (filled, total) == (30, 30)

def test_certificate_keeps_theorem_closure_closed():
    cert = json.loads(CERT.read_text())
    assert cert["status"] == "FINITE_DATA_COMPLETE_NO_THEOREM_CLOSURE"
    assert cert["closure_state"]["closure_ready"] is False
    assert cert["closure_state"]["strict_completion_status"] == "NOT_READY"

def test_progressive_packet_keeps_strict_gate_closed_after_finite_data_completion():
    progressive = json.loads(PROGRESSIVE.read_text())
    assert progressive["closure_ready"] is False
    assert progressive["strict_completion_status"] == "NOT_READY"
    for key in ["R1", "R2", "R3"]:
        assert progressive["targets"][key]["state"] == "SUPPLIED"
        assert progressive["targets"][key]["verification_result"] == "FINITE_DATA_CHECKER_SUPPLIED_NOT_LEAN_PROOF"

def test_certificate_names_next_missing_proof_objects():
    cert = json.loads(CERT.read_text())
    missing = set(cert["next_missing_objects"])
    assert "R1_LEAN_PROOF_ARTIFACT" in missing
    assert "R2_LEAN_PROOF_ARTIFACT" in missing
    assert "R3_LEAN_PROOF_ARTIFACT" in missing
    assert "REPOSITORY_NATIVE_R1_R2_R3_INSTANCE" in missing
    assert "REPOSITORY_NATIVE_R1_R2_R3_BINDING_CLOSURE" in missing
