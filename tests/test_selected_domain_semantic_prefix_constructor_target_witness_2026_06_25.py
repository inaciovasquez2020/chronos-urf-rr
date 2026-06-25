import subprocess, sys

def test_verifier_passes():
    subprocess.run(
        [sys.executable,
         "tools/verify_selected_domain_semantic_prefix_constructor_target_witness_2026_06_25.py"],
        check=True,
    )
