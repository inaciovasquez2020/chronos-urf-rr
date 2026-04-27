import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_petersen_fgl_export_certifies_kernel_containment():
    p = subprocess.run(
        [sys.executable, str(ROOT / "tools/export_fgl_from_petersen_2lift.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, p.stderr + p.stdout

    source = json.loads((ROOT / "artifacts/fgl/source_matrices.json").read_text())
    assert source["field"] == "GF(2)"
    assert source["metadata"]["cycle_space_dimension"] == 11
    assert source["metadata"]["local_cycle_span_dimension"] == 10
    assert source["metadata"]["quotient_dimension"] == 1
    assert len(source["test_matrix_basis_by_test"]) == 11
    assert len(source["test_matrix_basis_by_test"][0]) == 1
    assert len(source["witness_matrix"]) == 11
    assert len(source["witness_matrix"][0]) == 10

    p = subprocess.run(
        [sys.executable, str(ROOT / "tools/export_fgl_matrices.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, p.stderr + p.stdout

    p = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools/certify_fgl.py"),
            str(ROOT / "artifacts/fgl/finite_patch_matrices.json"),
            str(ROOT / "artifacts/fgl/fgl_certificate.json"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, p.stderr + p.stdout

    cert = json.loads((ROOT / "artifacts/fgl/fgl_certificate.json").read_text())
    assert cert["field"] == "GF(2)"
    assert cert["basis_size"] == 11
    assert cert["kernel_contained_in_witness"] is True
    assert cert["annihilates_witness"] is True
    assert cert["quotient_rank_valid"] is True
    assert cert["status"] == "Proved"
