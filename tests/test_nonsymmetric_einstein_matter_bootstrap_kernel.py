import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_nonsymmetric_einstein_matter_bootstrap_kernel_verifier_passes():
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools/verify_nonsymmetric_einstein_matter_bootstrap_kernel.py"),
        ],
        check=True,
        cwd=ROOT,
    )
