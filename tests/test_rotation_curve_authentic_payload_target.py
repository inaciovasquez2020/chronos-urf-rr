from pathlib import Path
import subprocess


def test_rotation_curve_authentic_payload_target_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_rotation_curve_authentic_payload_target.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ROTATION_CURVE_AUTHENTIC_PAYLOAD_TARGET_OK" in result.stdout
