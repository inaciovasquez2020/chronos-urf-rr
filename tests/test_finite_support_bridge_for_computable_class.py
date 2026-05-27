import subprocess

def test_finite_support_bridge_for_computable_class_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_finite_support_bridge_for_computable_class.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "FINITE_SUPPORT_BRIDGE_FOR_COMPUTABLE_CLASS_OK" in result.stdout
