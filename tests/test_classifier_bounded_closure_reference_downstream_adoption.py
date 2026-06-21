import subprocess
import sys


def test_classifier_bounded_closure_reference_downstream_adoption_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_classifier_bounded_closure_reference_downstream_adoption.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "CLASSIFIER_BOUNDED_CLOSURE_REFERENCE_DOWNSTREAM_ADOPTION_OK" in result.stdout
