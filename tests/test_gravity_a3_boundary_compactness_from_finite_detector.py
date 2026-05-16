import subprocess


def test_gravity_a3_boundary_compactness_from_finite_detector_verifier():
    subprocess.run(
        ["python3", "tools/verify_gravity_a3_boundary_compactness_from_finite_detector.py"],
        check=True,
    )
