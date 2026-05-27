import subprocess


def test_named_concrete_natural_admissibility_certificate_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_named_concrete_natural_admissibility_certificate.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NAMED_CONCRETE_NATURAL_ADMISSIBILITY_CERTIFICATE_OK" in result.stdout
