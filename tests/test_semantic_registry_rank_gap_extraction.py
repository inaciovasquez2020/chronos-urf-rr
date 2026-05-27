import subprocess

def test_semantic_registry_rank_gap_extraction_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_semantic_registry_rank_gap_extraction.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SEMANTIC_REGISTRY_RANK_GAP_EXTRACTION_OK" in result.stdout
