import subprocess
import sys

def test_newtonian_force_detector_coherence_bridge():
    subprocess.run(
        [sys.executable, "tools/verify_newtonian_force_detector_coherence_bridge.py"],
        check=True,
    )
