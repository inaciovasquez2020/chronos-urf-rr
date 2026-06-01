import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/predeclared_comparison_metric_2026_06_01.json")
DOC = Path("docs/status/PREDECLARED_COMPARISON_METRIC_2026_06_01.md")
VERIFY = Path("tools/verify_predeclared_comparison_metric.py")

def test_artifact_records_predeclared_comparison_metric():
    data = json.loads(ART.read_text())
    assert data["object"] == "PREDECLARED_COMPARISON_METRIC"
    assert data["decision"] == "PASS"
    assert data["resolved_missing_input"] == "predeclared_comparison_metric"

def test_metric_is_canonical_rmse():
    data = json.loads(ART.read_text())
    metric = data["predeclared_metric"]
    assert metric["metric_id"] == "canonical_rmse_between_aligned_vectors_v1"
    assert metric["primary_metric"] == "canonical_rmse"
    assert metric["metric_direction"] == "lower_is_better"
    assert metric["vector_length"] > 0

def test_remaining_missing_input_is_run_output():
    data = json.loads(ART.read_text())
    assert data["remaining_missing_input_count"] == 1
    assert data["remaining_missing_inputs"] == ["reproducible_comparison_run_output"]

def test_doc_preserves_boundary():
    doc = DOC.read_text()
    assert "predeclared comparison metric only" in doc
    assert "no reproducible comparison run output supplied" in doc
    assert "no Clay-problem claim" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "PREDECLARED_COMPARISON_METRIC_OK" in result.stdout
