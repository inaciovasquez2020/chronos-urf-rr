import subprocess


def test_boundary_nuclearity_from_finite_detector_algebra_verifier():
    subprocess.run(
        ["python3", "tools/verify_boundary_nuclearity_from_finite_detector_algebra.py"],
        check=True,
    )
