import subprocess


def test_gravity_finite_state_boundary_compactness_certificate_verifier():
    subprocess.run(
        ["python3", "tools/verify_gravity_finite_state_boundary_compactness_certificate.py"],
        check=True,
    )
