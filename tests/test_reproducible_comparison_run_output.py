import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/reproducible_comparison_run_output_2026_06_01.json")
DOC = Path("docs/status/REPRODUCIBLE_COMPARISON_RUN_OUTPUT_2026_06_01.md")
VERIFY = Path("tools/verify_reproducible_comparison_run_output.py")

def test_artifact_records_reproducible_run_output():
    data = json.loads(ART.read_text())
    assert data["object"] == "REPRODUCIBLE_COMPARISON_RUN_OUTPUT"
    assert data["decision"] == "PASS"
    assert data["resolved_missing_input"] == "reproducible_comparison_run_output"

def test_metrics_are_present():
    data = json.loads(ART.read_text())
    assert data["metric_id"] == "canonical_rmse_between_aligned_vectors_v1"
    assert data["primary_metric"] == "canonical_rmse"
    assert data["vector_length"] == 4096
    assert "canonical_rmse" in data
    assert "canonical_mae" in data
    assert "run_output_sha256" in data

def test_remaining_missing_inputs_are_zero():
    data = json.loads(ART.read_text())
    assert data["remaining_missing_inputs"] == []
    assert data["remaining_missing_input_count"] == 0

def test_doc_preserves_boundary():
    doc = DOC.read_text()
    assert "This packet records run output only." in doc
    assert "empirical gravity result interpretation" in doc
    assert "Clay-problem claim" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "REPRODUCIBLE_COMPARISON_RUN_OUTPUT_OK" in result.stdout
