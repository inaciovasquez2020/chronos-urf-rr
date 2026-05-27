import subprocess


def test_first_target_natural_admissibility_certificate_frontier_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_first_target_natural_admissibility_certificate_frontier.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "FIRST_TARGET_NATURAL_ADMISSIBILITY_CERTIFICATE_FRONTIER_OK" in result.stdout
