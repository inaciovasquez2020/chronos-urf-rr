import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/authentic_mascon_comparison_metric_2026_05_30.json"

def test_authentic_mascon_comparison_metric_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_authentic_mascon_comparison_metric.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "AUTHENTIC_MASCON_COMPARISON_METRIC_OK" in result.stdout

def test_authentic_mascon_comparison_metric_recorded_without_empirical_result():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    assert artifact["metric"]["metric_supplied"] is True
    assert artifact["metric"]["same_unit_comparison"] is True
    assert artifact["metric"]["empirical_comparison_executed"] is False
    assert artifact["boundary"]["empirical_gravity_result_claimed"] is False
