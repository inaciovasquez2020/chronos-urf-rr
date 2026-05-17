import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_rate_thick_conditional_reduction_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_rate_thick_conditional_reduction_only.py"],
        cwd=ROOT,
        check=True,
    )

def test_rate_thick_status_is_conditional_reduction_only():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/rate_thick_conditional_reduction_only_2026_05_17.json").read_text()
    )
    assert artifact["status"] == "CONDITIONAL_REDUCTION_ONLY"
    assert "DimensionRegularFiberGrowth" in artifact["missing_lemmas"]
    assert "RankRateToLyapunovExpansion" in artifact["missing_lemmas"]
    assert "FiberEntropyMassLowerBoundsUnstableEntropy" in artifact["missing_lemmas"]
