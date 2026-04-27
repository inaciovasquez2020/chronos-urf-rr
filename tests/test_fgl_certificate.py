import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cert(input_path: Path, output_path: Path):
    if output_path.exists():
        output_path.unlink()
    p = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools/certify_fgl.py"),
            str(input_path),
            str(output_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    data = json.loads(output_path.read_text()) if output_path.exists() else None
    return p, data


def test_fgl_certificate_passes_kernel_containment(tmp_path):
    src = tmp_path / "example_pass.json"
    out = tmp_path / "out_pass.json"

    src.write_text(
        json.dumps(
            {
                "field": "Q",
                "test_matrix_basis_by_test": [
                    [0],
                    [0],
                    [1],
                ],
                "witness_matrix": [
                    [1, 0],
                    [0, 1],
                    [0, 0],
                ],
            }
        ),
        encoding="utf-8",
    )

    p, data = run_cert(src, out)
    assert p.returncode == 0, p.stderr + p.stdout
    assert data["status"] == "Proved"
    assert data["kernel_contained_in_witness"] is True
    assert data["annihilates_witness"] is True
    assert data["quotient_rank_valid"] is True


def test_fgl_certificate_fails_when_kernel_not_contained(tmp_path):
    src = tmp_path / "example_fail.json"
    out = tmp_path / "out_fail.json"

    src.write_text(
        json.dumps(
            {
                "field": "Q",
                "test_matrix_basis_by_test": [
                    [1],
                    [0],
                    [0],
                ],
                "witness_matrix": [
                    [1],
                    [0],
                    [0],
                ],
            }
        ),
        encoding="utf-8",
    )

    p, data = run_cert(src, out)
    assert p.returncode == 10
    assert data["status"] == "Conditional"
    assert data["kernel_contained_in_witness"] is False
