import subprocess
from pathlib import Path

ROOT = Path.cwd()


def test_repository_native_finite_registry_exhaustiveness_independent_verifier():
    subprocess.run(
        ["python3", "tools/verify_repository_native_finite_registry_exhaustiveness_independent.py"],
        cwd=ROOT,
        check=True,
    )
