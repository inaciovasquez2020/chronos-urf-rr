import subprocess

def test_r1_restricted_long_chord_safe_admissibility_verifier():
    subprocess.run(
        ["python3", "tools/verify_r1_restricted_long_chord_safe_admissibility.py"],
        check=True,
    )
