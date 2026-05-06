import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "Chronos" / "Core" / "TraceRegimeClassifier.lean"
VERIFY = ROOT / "tools" / "verify_chronos_trace_regime_classifier.py"

def test_trace_regime_classifier_tokens():
    text = LEAN.read_text()
    assert "ZAP2_REGIME_CLOSED" in text
    assert "AFFINE_LINEAR_ADMISSIBLE" in text
    assert "AFFINE_SUBLINEAR_FORBIDDEN" in text
    assert "AFFINE_INTERMEDIATE_FRONTIER_OPEN" in text
    assert "UNKNOWN_FRONTIER_OPEN" in text
    assert "ChronosTraceManifest_2026_05_05_audit" in text
    assert "ChronosTraceClassifierCompleteness" in text

def test_trace_regime_classifier_boundary_language():
    text = LEAN.read_text()
    forbidden = [
        "P vs NP solved",
        "P≠NP proved",
        "H4.1 proved",
        "FGL proved",
        "canonical Chronos closure",
        "theoremClosure true",
    ]
    for token in forbidden:
        assert token not in text

def test_trace_regime_classifier_verifier():
    subprocess.run([str(VERIFY)], cwd=ROOT, check=True)
