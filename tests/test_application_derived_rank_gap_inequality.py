import subprocess

def test_application_derived_rank_gap_inequality_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_application_derived_rank_gap_inequality.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "APPLICATION_DERIVED_RANK_GAP_INEQUALITY_OK" in result.stdout
