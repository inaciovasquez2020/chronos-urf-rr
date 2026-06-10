import subprocess

def test_external_genuine_analytic_dini_payload_theorem1_theorem2_verifier():
    subprocess.run(
        ["python3", "tools/verify_external_genuine_analytic_dini_payload_theorem1_theorem2.py"],
        check=True,
    )
