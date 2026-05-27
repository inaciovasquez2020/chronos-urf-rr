import subprocess

def test_dominance_admissible_computable_class_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_dominance_admissible_computable_class.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DOMINANCE_ADMISSIBLE_COMPUTABLE_CLASS_OK" in result.stdout
