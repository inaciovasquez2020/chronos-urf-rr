import subprocess
from pathlib import Path


def test_ytr_gravity_elastic_real_data_evidence_target_verifier():
    root = Path(__file__).resolve().parents[1]
    subprocess.run(
        ["python3", "tools/verify_ytr_gravity_elastic_real_data_evidence_target.py"],
        cwd=root,
        check=True,
    )
