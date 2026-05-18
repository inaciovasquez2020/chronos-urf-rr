import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_admissible_pnp_boundary_lock_to_clay_boundary_lock_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_admissible_pnp_boundary_lock_to_clay_boundary_lock.py"],
        cwd=ROOT,
        check=True,
    )

def test_admissible_pnp_boundary_lock_to_clay_boundary_lock_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/admissible_pnp_boundary_lock_to_clay_boundary_lock_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "ADMISSIBLE_CLAY_BOUNDARY_LOCK_CLOSED_NO_THEOREM_PROMOTION"
    boundary = "\n".join(artifact["boundary"])
    assert "admissible restricted Clay boundary lock only" in boundary
    assert "does not prove P vs NP" in boundary
    assert "does not refute P vs NP" in boundary
    assert "does not prove any Clay problem" in boundary
    assert "does not refute any Clay problem" in boundary

def test_admissible_pnp_boundary_lock_to_clay_boundary_lock_lean_surface_has_no_sorry():
    lean = (ROOT / "lean/Chronos/Frontier/AdmissiblePNPBoundaryLockToClayBoundaryLock.lean").read_text()
    assert "theorem AdmissiblePNPBoundaryLockToClayBoundaryLock_solved" in lean
    assert "theorem AdmissibleClayBoundaryLockTarget_solved" in lean
    assert "theorem clay_boundary_status_frontier_open" in lean
    assert "ClayStatus.frontier_open" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
