import subprocess

def test_repository_native_semantic_registry_computation_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_repository_native_semantic_registry_computation.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "REPOSITORY_NATIVE_SEMANTIC_REGISTRY_COMPUTATION_OK" in result.stdout
