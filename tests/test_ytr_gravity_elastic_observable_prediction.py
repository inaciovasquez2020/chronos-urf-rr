import subprocess
import sys


def test_ytr_gravity_elastic_observable_prediction_verifier():
    result = subprocess.run(
        [sys.executable, "tools/verify_ytr_gravity_elastic_observable_prediction.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "YTR_GRAVITY_ELASTIC_OBSERVABLE_PREDICTION_OK" in result.stdout
