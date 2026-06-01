import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/model_or_deficit_mass_vector_2026_06_01.json")
DOC = Path("docs/status/MODEL_OR_DEFICIT_MASS_VECTOR_2026_06_01.md")
VERIFY = Path("tools/verify_model_or_deficit_mass_vector.py")

def test_artifact_records_model_or_deficit_mass_vector():
    data = json.loads(ART.read_text())
    assert data["object"] == "MODEL_OR_DEFICIT_MASS_VECTOR"
    assert data["decision"] == "PASS"
    assert data["resolved_missing_input"] == "model_or_deficit_mass_vector"

def test_vector_is_aligned_zero_null_vector():
    data = json.loads(ART.read_text())
    vec = data["model_or_deficit_mass_vector"]
    assert vec["length"] == len(vec["values"])
    assert vec["length"] > 0
    assert all(float(x) == 0.0 for x in vec["values"])
    assert vec["sha256"]

def test_remaining_missing_inputs_are_three():
    data = json.loads(ART.read_text())
    assert data["remaining_missing_input_count"] == 3
    assert "unit_conversion_certificate" in data["remaining_missing_inputs"]
    assert "predeclared_comparison_metric" in data["remaining_missing_inputs"]
    assert "reproducible_comparison_run_output" in data["remaining_missing_inputs"]

def test_doc_preserves_boundary():
    doc = DOC.read_text()
    assert "aligned zero null vector only" in doc
    assert "not a DFM-MKC physical model vector" in doc
    assert "no empirical gravity result supplied" in doc
    assert "no Clay-problem claim" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MODEL_OR_DEFICIT_MASS_VECTOR_OK" in result.stdout
