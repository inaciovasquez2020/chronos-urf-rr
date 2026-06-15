import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/r1a_trivial_two_face_boundary_statement_surface_2026_06_15.json"
VERIFIER = ROOT / "tools/verify_r1a_trivial_two_face_boundary_statement_surface.py"


def test_r1a_trivial_two_face_boundary_statement_surface_verifies():
    result = subprocess.run(
        ["python3", str(VERIFIER)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "R1A_TRIVIAL_TWO_FACE_BOUNDARY_STATEMENT_SURFACE_OK" in result.stdout


def test_r1a_trivial_two_face_boundary_statement_surface_rejects_overclaim(tmp_path):
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    data["boundary"]["proof_claims"]["proves_r1a"] = True
    bad_artifact = tmp_path / "bad_r1a_statement_surface.json"
    bad_artifact.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

    result = subprocess.run(
        ["python3", str(VERIFIER), str(bad_artifact)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "overclaiming proof flag: proves_r1a" in result.stderr
