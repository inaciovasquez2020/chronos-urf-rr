import subprocess


def test_gravity_physical_to_topological_compactness_certificate_verifier():
    subprocess.run(
        ["python3", "tools/verify_gravity_physical_to_topological_compactness_certificate.py"],
        check=True,
    )
