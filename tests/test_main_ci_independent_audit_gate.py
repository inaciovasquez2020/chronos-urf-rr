import subprocess


def test_main_ci_independent_audit_gate():
    result = subprocess.run(
        ["python3", "tools/verify_main_ci_independent_audit_gate.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MAIN_CI_INDEPENDENT_AUDIT_GATE_OK" in result.stdout
