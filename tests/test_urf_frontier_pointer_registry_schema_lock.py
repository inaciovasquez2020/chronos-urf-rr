import subprocess
import sys

def test_urf_frontier_pointer_registry_schema_lock():
    r = subprocess.run(
        [sys.executable, "scripts/check_urf_frontier_pointer_registry_schema_lock.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "urf-frontier-pointer-registry-schema-lock: PASS" in r.stdout
