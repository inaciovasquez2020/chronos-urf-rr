import subprocess

def test_concrete_non_toy_application_rank_gap_extraction_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_concrete_non_toy_application_rank_gap_extraction.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CONCRETE_NON_TOY_APPLICATION_RANK_GAP_EXTRACTION_OK" in result.stdout
