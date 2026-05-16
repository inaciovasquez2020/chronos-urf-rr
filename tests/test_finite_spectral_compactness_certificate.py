import subprocess
import sys
from pathlib import Path


def test_finite_spectral_compactness_certificate_verifier():
    root = Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, "tools/verify_finite_spectral_compactness_certificate.py"],
        cwd=root,
        check=True,
    )
