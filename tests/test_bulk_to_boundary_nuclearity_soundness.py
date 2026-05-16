import subprocess


def test_bulk_to_boundary_nuclearity_soundness_verifier():
    subprocess.run(
        ["python3", "tools/verify_bulk_to_boundary_nuclearity_soundness.py"],
        check=True,
    )
