import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_target_interface_compatibility_proof_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/target_interface_compatibility_proof_2026_06_11.json").read_text()
    )
    assert data["name"] == "TARGET_INTERFACE_COMPATIBILITY_PROOF"
    assert data["status"] == "PROOF_OBLIGATION_SURFACE_ONLY_NO_TARGET_INTERFACE_COMPATIBILITY_PROOF"
    assert data["previous_object"] == "PACKAGE_COMPATIBILITY_PROOF"
    assert data["next_admissible_object"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF"
    assert "no unconditional target-interface compatibility theorem" in data["boundary"]
    assert "no concrete analytic Einstein-matter estimate package proof" in data["boundary"]

def test_target_interface_compatibility_proof_doc():
    text = (ROOT / "docs/status/TARGET_INTERFACE_COMPATIBILITY_PROOF_2026_06_11.md").read_text()
    assert "TARGET_INTERFACE_COMPATIBILITY_PROOF" in text
    assert "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF" in text
    assert "unconditional target-interface compatibility theorem" in text

def test_target_interface_compatibility_proof_lean_surface():
    text = (ROOT / "lean/Chronos/Frontier/TargetInterfaceCompatibilityProof.lean").read_text()
    assert "structure TargetInterfaceCompatibilityProofSurfaceData" in text
    assert "structure TargetInterfaceCompatibilityProofSurfaceObligations" in text
    assert "theorem TargetInterfaceCompatibilityProofSurface" in text
    assert "PROOF_OBLIGATION_SURFACE_ONLY_NO_TARGET_INTERFACE_COMPATIBILITY_PROOF" in text
