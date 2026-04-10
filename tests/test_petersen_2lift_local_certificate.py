import json
import subprocess
import sys

def test_petersen_2lift_local_certificate():
    proc = subprocess.run(
        [sys.executable, "scripts/check_petersen_2lift_local_certificate.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["radius"] == 2
    assert data["pairs_checked"] == 10
    assert data["local_property_checked"] is False
    assert any(item.get("same_profile") is False for item in data["certificate"])
