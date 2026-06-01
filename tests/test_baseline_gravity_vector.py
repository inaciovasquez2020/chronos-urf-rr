import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/baseline_gravity_vector_2026_06_01.json")
DOC = Path("docs/status/BASELINE_GRAVITY_VECTOR_2026_06_01.md")
VERIFY = Path("tools/verify_baseline_gravity_vector.py")

def test_artifact_records_baseline_vector():
    data = json.loads(ART.read_text())
    assert data["object"] == "BASELINE_GRAVITY_VECTOR"
    assert data["decision"] == "PASS"
    assert data["resolved_missing_input"] == "baseline_gravity_vector"

def test_baseline_vector_is_nonempty_and_bounded():
    data = json.loads(ART.read_text())
    vec = data["baseline_vector"]
    assert vec["length"] == len(vec["values"])
    assert 0 < vec["length"] <= 4096
    assert vec["sha256"]

def test_remaining_missing_inputs_are_four():
    data = json.loads(ART.read_text())
    assert data["remaining_missing_input_count"] == 4
    assert "model_or_deficit_mass_vector" in data["remaining_missing_inputs"]
    assert "reproducible_comparison_run_output" in data["remaining_missing_inputs"]

def test_doc_preserves_boundary():
    doc = DOC.read_text()
    assert "baseline gravity vector only" in doc
    assert "no empirical gravity result supplied" in doc
    assert "no Clay-problem claim" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "BASELINE_GRAVITY_VECTOR_OK" in result.stdout
