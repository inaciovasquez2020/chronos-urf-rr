import subprocess
from pathlib import Path


def test_ytr_gravity_elastic_nontriviality_certificate_verifier():
    root = Path(__file__).resolve().parents[1]
    subprocess.run(
        ["python3", "tools/verify_ytr_gravity_elastic_nontriviality_certificate.py"],
        cwd=root,
        check=True,
    )
