import subprocess

def test_certificate_supply_law_for_computable_class_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_certificate_supply_law_for_computable_class.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CERTIFICATE_SUPPLY_LAW_FOR_COMPUTABLE_CLASS_OK" in result.stdout
