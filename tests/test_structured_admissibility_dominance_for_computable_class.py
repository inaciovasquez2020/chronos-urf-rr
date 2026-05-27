import subprocess

def test_structured_admissibility_dominance_for_computable_class_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_structured_admissibility_dominance_for_computable_class.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "STRUCTURED_ADMISSIBILITY_DOMINANCE_FOR_COMPUTABLE_CLASS_OK" in result.stdout
