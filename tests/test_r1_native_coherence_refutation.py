import subprocess

def test_r1_native_coherence_refutation_verifier():
    subprocess.run(
        ["python3", "tools/verify_r1_native_coherence_refutation.py"],
        check=True,
    )
