import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_selected_domain_h41_fgl_to_admissible_h41_fgl_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_selected_domain_h41_fgl_to_admissible_h41_fgl.py"],
        cwd=ROOT,
        check=True,
    )
