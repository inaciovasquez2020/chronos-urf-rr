import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_admissible_chronos_rr_to_h41_fgl_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_admissible_chronos_rr_to_h41_fgl.py"],
        cwd=ROOT,
        check=True,
    )

def test_admissible_chronos_rr_to_h41_fgl_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/admissible_chronos_rr_to_h41_fgl_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "ADMISSIBLE_H41_FGL_TARGET_CLOSED_RESTRICTED_ONLY"
    boundary = "\n".join(artifact["boundary"])
    assert "admissible restricted H4.1/FGL target only" in boundary
    assert "does not prove unrestricted H4.1/FGL" in boundary
    assert "does not prove P vs NP" in boundary

def test_admissible_chronos_rr_to_h41_fgl_lean_surface_has_no_sorry():
    lean = (ROOT / "lean/Chronos/Frontier/AdmissibleChronosRRToH41FGL.lean").read_text()
    assert "theorem AdmissibleChronosRRToH41FGL_solved" in lean
    assert "theorem AdmissibleH41FGLTarget_solved" in lean
    assert "theorem UnrestrictedH41FGLTarget_refuted" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
