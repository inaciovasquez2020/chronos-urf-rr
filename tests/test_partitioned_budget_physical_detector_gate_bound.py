import json
import subprocess
from pathlib import Path

def test_verifier_passes():
    out = subprocess.check_output([
        "python3",
        "tools/verify_partitioned_budget_physical_detector_gate_bound.py",
    ], text=True)
    assert "PARTITIONED_BUDGET_PHYSICAL_DETECTOR_GATE_BOUND_OK" in out

def test_artifact_records_certificate_condition():
    data = json.loads(Path(
        "artifacts/chronos/partitioned_budget_physical_detector_gate_bound_2026_05_28.json"
    ).read_text())
    assert data["status"] == "DERIVED_GATE_BOUND_FROM_PARTITIONED_BUDGET_CERTIFICATE"
    assert "PartitionedPhysicalDetectorBudgetCertificate" in data["conditional_on"]
    assert "twoDetectorExample_closes_gate" in data["closed_theorems"]

def test_boundary_tokens_preserved():
    data = json.loads(Path(
        "artifacts/chronos/partitioned_budget_physical_detector_gate_bound_2026_05_28.json"
    ).read_text())
    assert "existence of a partitioned budget certificate for arbitrary physical detector fields" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
