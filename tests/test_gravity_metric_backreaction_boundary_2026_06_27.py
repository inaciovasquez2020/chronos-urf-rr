import subprocess

def test_gravity_metric_backreaction_boundary():
    result = subprocess.run(
        ["python3", "tools/verify_gravity_metric_backreaction_boundary_2026_06_27.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "GRAVITY_METRIC_BACKREACTION_BOUNDARY_2026_06_27_OK" in result.stdout
