import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cert(path: str):
    out = ROOT / "artifacts/fgl/test_out.json"
    if out.exists():
        out.unlink()
    p = subprocess.run(
        [sys.executable, str(ROOT / "tools/certify_fgl.py"), str(ROOT / path), str(out)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text()) if out.exists() else None
    return p, data


def test_fgl_certificate_passes_kernel_containment():
    p, data = run_cert("artifacts/fgl/example_pass.json")
    assert p.returncode == 0, p.stderr + p.stdout
    assert data["status"] == "Proved"
    assert data["kernel_contained_in_witness"] is True
    assert data["annihilates_witness"] is True
    assert data["quotient_rank_valid"] is True


def test_fgl_certificate_fails_when_kernel_not_contained():
    p, data = run_cert("artifacts/fgl/example_fail.json")
    assert p.returncode == 10
    assert data["status"] == "Conditional"
    assert data["kernel_contained_in_witness"] is False
