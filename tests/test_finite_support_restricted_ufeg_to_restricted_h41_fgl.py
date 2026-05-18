from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_verifier_passes():
    subprocess.run(["python3", "tools/verify_finite_support_restricted_ufeg_to_restricted_h41_fgl.py"], cwd=ROOT, check=True)

def test_files_present():
    assert (ROOT / "lean/Chronos/Frontier/FiniteSupportRestrictedUFEGToRestrictedH41FGL.lean").exists()
    assert (ROOT / "docs/status/FINITE_SUPPORT_RESTRICTED_UFEG_TO_RESTRICTED_H41FGL_2026_05_18.md").exists()
    assert (ROOT / "artifacts/chronos/finite_support_restricted_ufeg_to_restricted_h41_fgl_2026_05_18.json").exists()

def test_lean_surface_contains_requested_objects():
    text = (ROOT / "lean/Chronos/Frontier/FiniteSupportRestrictedUFEGToRestrictedH41FGL.lean").read_text()
    assert "structure FiniteSupportRestrictedUFEGToRestrictedH41FGLData" in text
    assert "def toRestrictedChronosRRData" in text
    assert "abbrev FiniteSupportRestrictedUFEG" in text
    assert "abbrev FiniteSupportRestrictedH41FGL" in text
    assert "theorem finite_support_restricted_ufeg_to_restricted_chronos_rr" in text
    assert "theorem finite_support_restricted_ufeg_to_restricted_h41_fgl" in text
    assert "theorem FiniteSupportRestrictedUFEGToRestrictedH41FGL" in text
    assert "RestrictedChronosRRToRestrictedH41FGL" in text
    assert "sorry" not in text
    assert "admit" not in text
    assert "axiom" not in text

def test_boundary_doc():
    text = (ROOT / "docs/status/FINITE_SUPPORT_RESTRICTED_UFEG_TO_RESTRICTED_H41FGL_2026_05_18.md").read_text()
    assert "Status: `FINITE_SUPPORT_RESTRICTED_H41FGL_TARGET_CLOSED_ONLY`" in text
    assert "finite-support admissible restricted domain only" in text
    assert "no unrestricted UniversalFiberEntropyGap" in text
    assert "no unrestricted Chronos-RR" in text
    assert "no unrestricted H4.1/FGL" in text
    assert "no P vs NP" in text
    assert "no Clay closure" in text

def test_artifact_status_and_boundary():
    data = json.loads((ROOT / "artifacts/chronos/finite_support_restricted_ufeg_to_restricted_h41_fgl_2026_05_18.json").read_text())
    assert data["status"] == "FINITE_SUPPORT_RESTRICTED_H41FGL_TARGET_CLOSED_ONLY"
    assert data["lean_theorem"] == "FiniteSupportRestrictedUFEGToRestrictedH41FGL"
    assert "FiniteSupportRestrictedUFEG -> RestrictedH41FGL" in data["closed"]
    assert "finite-support admissible restricted domain only" in data["boundary"]
    assert "no unrestricted UniversalFiberEntropyGap" in data["boundary"]
    assert "no unrestricted Chronos-RR" in data["boundary"]
    assert "no unrestricted H4.1/FGL" in data["boundary"]
    assert "no P vs NP" in data["boundary"]
    assert "no Clay closure" in data["boundary"]
