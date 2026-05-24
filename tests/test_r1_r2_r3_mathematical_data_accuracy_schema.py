import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "artifacts/chronos/r1_r2_r3_mathematical_data_accuracy_schema_2026_05_24.json"

def test_mathematical_data_accuracy_schema_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_r2_r3_mathematical_data_accuracy_schema.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "R1_R2_R3_MATHEMATICAL_DATA_ACCURACY_SCHEMA_OK" in result.stdout
    assert "structural_completeness=" in result.stdout

def test_accuracy_policy_makes_no_truth_claim():
    data = json.loads(SCHEMA.read_text())
    assert data["accuracy_policy"]["score_type"] == "STRUCTURAL_COMPLETENESS_ONLY"
    assert data["accuracy_policy"]["truth_accuracy_claim"] is False
    assert data["accuracy_policy"]["empirical_accuracy_claim"] is False
    assert data["accuracy_policy"]["theorem_accuracy_claim"] is False

def test_all_targets_have_required_mathematical_data_slots():
    data = json.loads(SCHEMA.read_text())
    required = data["accuracy_policy"]["minimum_verified_fields_per_target"]
    for target in data["targets"].values():
        for field in required:
            assert field in target

def test_schema_blocks_premature_overclaim_tokens():
    data = json.loads(SCHEMA.read_text())
    blocked = set(data["does_not_prove"])
    assert "mathematical accuracy" in blocked
    assert "LongChordExclusion" in blocked
    assert "DiameterSeparationFillingObstruction" in blocked
    assert "UniformLocalTypeCapacity" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
