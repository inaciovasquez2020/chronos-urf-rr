import subprocess

def test_r1_native_coherence_promotion_target_verifier():
    subprocess.run(
        ["python3", "tools/verify_r1_native_coherence_promotion_target.py"],
        check=True,
    )
