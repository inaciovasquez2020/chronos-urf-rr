import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_admissible_h41_fgl_to_pnp_boundary_lock_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_admissible_h41_fgl_to_pnp_boundary_lock.py"],
        cwd=ROOT,
        check=True,
    )

def test_admissible_h41_fgl_to_pnp_boundary_lock_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/admissible_h41_fgl_to_pnp_boundary_lock_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "ADMISSIBLE_PNP_BOUNDARY_LOCK_CLOSED_NO_THEOREM_PROMOTION"
    boundary = "\n".join(artifact["boundary"])
    assert "admissible restricted P vs NP boundary lock only" in boundary
    assert "does not prove P vs NP" in boundary
    assert "does not refute P vs NP" in boundary

def test_admissible_h41_fgl_to_pnp_boundary_lock_lean_surface_has_no_sorry():
    lean = (ROOT / "lean/Chronos/Frontier/AdmissibleH41FGLToPNPBoundaryLock.lean").read_text()
    assert "theorem AdmissibleH41FGLToPNPBoundaryLock_solved" in lean
    assert "theorem AdmissiblePNPBoundaryLockTarget_solved" in lean
    assert "theorem pnp_boundary_status_frontier_open" in lean
    assert "PNPStatus.frontier_open" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
