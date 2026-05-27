import subprocess


def test_natural_admissibility_to_dominance_class_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_natural_admissibility_to_dominance_class.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NATURAL_ADMISSIBILITY_TO_DOMINANCE_CLASS_OK" in result.stdout
