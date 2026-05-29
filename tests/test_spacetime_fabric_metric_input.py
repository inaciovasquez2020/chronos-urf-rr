import subprocess
import sys


def test_spacetime_fabric_metric_input() -> None:
    subprocess.run(
        [sys.executable, "tools/verify_spacetime_fabric_metric_input.py"],
        check=True,
    )
