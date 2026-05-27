import subprocess

def test_derived_finite_registered_hyperbolic_natural_admissibility_certificate_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_derived_finite_registered_hyperbolic_natural_admissibility_certificate.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DERIVED_FINITE_REGISTERED_HYPERBOLIC_NATURAL_ADMISSIBILITY_CERTIFICATE_OK" in result.stdout
