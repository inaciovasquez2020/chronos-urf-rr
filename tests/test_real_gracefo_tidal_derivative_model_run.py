import json
import subprocess
from pathlib import Path

def test_real_gracefo_tidal_derivative_model_run():
    result = subprocess.run(
        ["python3", "tools/verify_real_gracefo_tidal_derivative_model_run.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "REAL_GRACEFO_TIDAL_DERIVATIVE_MODEL_RUN_OK" in result.stdout

    artifact = Path("artifacts/gracefo/real_gracefo_tidal_derivative_model_run_2026_05_29.json")
    payload = json.loads(artifact.read_text())

    assert payload["status"] == "REAL_GRACEFO_TIDAL_DERIVATIVE_MODEL_RUN_CREATED"
    assert payload["period_count"] == 2
    assert payload["payload_record_count"] == 12
    assert payload["product_branch_count"] == 6
    assert payload["aggregate"]["mean_tidal_derivative_coefficient"] >= 0
