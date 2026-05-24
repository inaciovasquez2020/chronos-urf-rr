#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "artifacts/chronos/r1_r2_r3_finite_data_completion_certificate_2026_05_24.json"
SCHEMA = ROOT / "artifacts/chronos/r1_r2_r3_mathematical_data_accuracy_schema_2026_05_24.json"
PROGRESSIVE = ROOT / "artifacts/chronos/r1_r2_r3_progressive_witness_packet_2026_05_24.json"
DOC = ROOT / "docs/status/R1_R2_R3_FINITE_DATA_COMPLETION_CERTIFICATE_2026_05_24.md"

CHECKERS = [
    "tools/check_r1_long_chord_exclusion_mathematical_data_packet.py",
    "tools/check_r2_diameter_separation_filling_mathematical_data_packet.py",
    "tools/check_r3_uniform_local_type_capacity_mathematical_data_packet.py",
]

BOUNDARY = [
    "LongChordExclusion",
    "DiameterSeparationFillingObstruction",
    "UniformLocalTypeCapacity",
    "native R1/R2/R3 instance",
    "NON_FACTORISATION",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

def fail(msg: str) -> None:
    raise SystemExit(f"R1_R2_R3_FINITE_DATA_COMPLETION_CERTIFICATE_FAILED: {msg}")

def require(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)

def run_checker(path: str) -> None:
    result = subprocess.run(
        [sys.executable, path],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    require(result.returncode == 0, f"{path} failed: {result.stdout}{result.stderr}")

def structural_score(schema: dict) -> tuple[int, int]:
    required = schema["accuracy_policy"]["minimum_verified_fields_per_target"]
    filled = 0
    total = 0
    for target in schema["targets"].values():
        for field in required:
            total += 1
            if target[field] not in (None, [], {}, ""):
                filled += 1
    return filled, total

def main() -> None:
    for path in [CERT, SCHEMA, PROGRESSIVE, DOC]:
        require(path.exists(), f"missing {path}")

    cert = json.loads(CERT.read_text())
    schema = json.loads(SCHEMA.read_text())
    progressive = json.loads(PROGRESSIVE.read_text())
    doc = DOC.read_text()

    require(cert["artifact"] == "R1_R2_R3_FINITE_DATA_COMPLETION_CERTIFICATE", "wrong artifact")
    require(cert["status"] == "FINITE_DATA_COMPLETE_NO_THEOREM_CLOSURE", "wrong status")

    for checker in CHECKERS:
        run_checker(checker)

    filled, total = structural_score(schema)
    require((filled, total) == (30, 30), f"schema completeness is {filled}/{total}, expected 30/30")
    require(cert["structural_completeness"]["ratio"] == "30/30", "certificate ratio mismatch")

    for key in ["R1", "R2", "R3"]:
        target = progressive["targets"][key]
        require(target["state"] == "SUPPLIED", f"{key} must be SUPPLIED")
        require(target["verification_result"] == "FINITE_DATA_CHECKER_SUPPLIED_NOT_LEAN_PROOF", f"{key} wrong verification_result")

    require(progressive["closure_ready"] is False, "progressive closure_ready must remain false")
    require(progressive["strict_completion_status"] == "NOT_READY", "strict completion must remain NOT_READY")

    require(cert["closure_state"]["closure_ready"] is False, "certificate closure_ready must be false")
    require(cert["closure_state"]["strict_completion_status"] == "NOT_READY", "certificate strict status must be NOT_READY")

    for token in BOUNDARY:
        require(token in cert["does_not_prove"], f"missing certificate boundary: {token}")
        require(token in doc, f"missing doc boundary: {token}")

    print("R1_R2_R3_FINITE_DATA_COMPLETION_CERTIFICATE_OK")

if __name__ == "__main__":
    main()
