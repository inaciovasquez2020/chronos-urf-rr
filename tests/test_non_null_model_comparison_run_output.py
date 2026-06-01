import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/non_null_model_comparison_run_output_2026_06_01.json")
DOC = Path("docs/status/NON_NULL_MODEL_COMPARISON_RUN_OUTPUT_2026_06_01.md")
VERIFY = Path("tools/verify_non_null_model_comparison_run_output.py")

def test_artifact_records_run_output():
    data = json.loads(ART.read_text())
    assert data["object"] == "NON_NULL_MODEL_COMPARISON_RUN_OUTPUT"
    assert data["decision"] == "PASS"
    assert data["resolved_missing_input"] == "NonNullModelComparisonRunOutput"

def test_metrics_present():
    data = json.loads(ART.read_text())
    assert data["metric_id"] == "canonical_rmse_between_aligned_vectors_v1"
    assert data["primary_metric"] == "canonical_rmse"
    assert data["vector_length"] == 4096
    assert "canonical_rmse" in data
    assert "run_output_sha256" in data

def test_doc_preserves_boundary():
    doc = DOC.read_text()
    assert "non-null model comparison run output only" in doc
    assert "model vector is derived from the observed LWE baseline" in doc
    assert "no empirical gravity result interpretation supplied" in doc
    assert "no Clay-problem claim" in doc

def test_next_object():
    data = json.loads(ART.read_text())
    assert data["next_admissible_object"] == "NON_NULL_MODEL_RESULT_INTERPRETATION"

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "NON_NULL_MODEL_COMPARISON_RUN_OUTPUT_OK" in result.stdout
