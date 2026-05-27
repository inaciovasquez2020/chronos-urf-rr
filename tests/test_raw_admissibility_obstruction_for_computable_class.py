import subprocess

def test_raw_admissibility_obstruction_for_computable_class_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_raw_admissibility_obstruction_for_computable_class.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "RAW_ADMISSIBILITY_OBSTRUCTION_FOR_COMPUTABLE_CLASS_OK" in result.stdout
