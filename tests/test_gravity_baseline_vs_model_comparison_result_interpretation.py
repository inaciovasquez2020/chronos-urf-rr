import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/gravity_baseline_vs_model_comparison_result_interpretation_2026_06_01.json")
DOC = Path("docs/status/GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_INTERPRETATION_2026_06_01.md")
VERIFY = Path("tools/verify_gravity_baseline_vs_model_comparison_result_interpretation.py")

def test_artifact_records_interpretation():
    data = json.loads(ART.read_text())
    assert data["object"] == "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_INTERPRETATION"
    assert data["decision"] == "PASS"
    assert data["interpretation"]["result_class"] == "null_comparator_residual_recorded"

def test_no_favored_or_empirical_claim():
    data = json.loads(ART.read_text())
    assert data["interpretation"]["favored_result"] == "none"
    assert data["interpretation"]["empirical_claim"] == "none"
    assert data["model_classification"]["not_physical_model"] is True

def test_remaining_missing_inputs_are_zero():
    data = json.loads(ART.read_text())
    assert data["remaining_missing_inputs"] == []
    assert data["remaining_missing_input_count"] == 0

def test_doc_preserves_boundary():
    doc = DOC.read_text()
    assert "comparison result interpretation only" in doc
    assert "null comparator residual" in doc
    assert "DFM-MKC validation" in doc
    assert "Clay-problem result" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_INTERPRETATION_OK" in result.stdout
