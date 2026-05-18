from pathlib import Path
import json
import subprocess
ROOT = Path(__file__).resolve().parents[1]
def test_verifier_passes():
    subprocess.run(["python3", "tools/verify_restricted_chronos_rr_to_restricted_h41fgl.py"], cwd=ROOT, check=True)
def test_artifact_status_and_boundary():
    artifact = json.loads((ROOT / "artifacts/chronos/restricted_chronos_rr_to_restricted_h41fgl_2026_05_18.json").read_text())
    assert artifact["target"] == "RestrictedChronosRRToRestrictedH41FGL"
    assert artifact["status"] == "RESTRICTED_CHRONOS_RR_TO_RESTRICTED_H41FGL_CLOSED"
    assert artifact["closed_theorem"] == "restricted_chronos_rr_to_restricted_h41_fgl"
    boundary = "\n".join(artifact["boundary"])
    assert "Restricted H4.1/FGL witness only" in boundary
    assert "restricted-domain bridge only" in boundary
    assert "unrestricted Chronos-RR remains FRONTIER_OPEN" in boundary
    assert "no unrestricted Chronos-RR" in boundary
    assert "no unrestricted H4.1/FGL theorem-level closure" in boundary
    assert "no Clay-problem closure" in boundary
def test_lean_surface_contains_requested_objects():
    text = (ROOT / "lean/Chronos/Frontier/RestrictedChronosRRToRestrictedH41FGL.lean").read_text()
    assert "abbrev RestrictedChronosRR" in text
    assert "structure RestrictedH41FGLWitness" in text
    assert "def RestrictedH41FGL" in text
    assert "theorem restricted_chronos_rr_to_restricted_h41_fgl" in text
    assert "rr_certificate : RestrictedChronosRR D" in text
    assert "boundary_lock : UnrestrictedChronosRRFrontierOpen" in text
    assert "unrestricted_chronos_rr_frontier_open" in text
    assert "def H41FGL" not in text
    assert "structure H41FGL" not in text
    assert "theorem unrestricted_chronos_rr " not in text
    assert "admit" not in text
    assert "sorry" not in text
    assert "axiom" not in text
def test_verifier_rejects_unrestricted_chronos_rr_overclaim():
    verifier = (ROOT / "tools/verify_restricted_chronos_rr_to_restricted_h41fgl.py").read_text()
    assert "unrestricted Chronos-RR is proved" in verifier
    assert "unrestricted Chronos-RR proved" in verifier
    assert "unrestricted Chronos-RR closed" in verifier
    assert "theorem unrestricted_chronos_rr " in verifier
def test_verifier_rejects_h41_fgl_solved_overclaim():
    verifier = (ROOT / "tools/verify_restricted_chronos_rr_to_restricted_h41fgl.py").read_text()
    assert "H4.1/FGL is solved" in verifier
    assert "H4.1/FGL solved" in verifier
    assert "H4.1/FGL is proved" in verifier
