import subprocess
import sys


def test_ytr_gravity_elastic_standard_gr_comparison_verifier():
    result = subprocess.run(
        [sys.executable, "tools/verify_ytr_gravity_elastic_standard_gr_comparison.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "YTR_GRAVITY_ELASTIC_STANDARD_GR_COMPARISON_OK" in result.stdout
