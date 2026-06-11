import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_package_compatibility_proof_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/package_compatibility_proof_2026_06_11.json").read_text()
    )
    assert data["name"] == "PACKAGE_COMPATIBILITY_PROOF"
    assert data["status"] == "PROOF_OBLIGATION_SURFACE_ONLY_NO_PACKAGE_COMPATIBILITY_PROOF"
    assert data["previous_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF"
    assert data["next_admissible_object"] == "TARGET_INTERFACE_COMPATIBILITY_PROOF"
    assert "no unconditional package compatibility theorem" in data["boundary"]
    assert "no concrete analytic Einstein-matter estimate package proof" in data["boundary"]

def test_package_compatibility_proof_doc():
    text = (ROOT / "docs/status/PACKAGE_COMPATIBILITY_PROOF_2026_06_11.md").read_text()
    assert "PACKAGE_COMPATIBILITY_PROOF" in text
    assert "TARGET_INTERFACE_COMPATIBILITY_PROOF" in text
    assert "unconditional package compatibility theorem" in text

def test_package_compatibility_proof_lean_surface():
    text = (ROOT / "lean/Chronos/Frontier/PackageCompatibilityProof.lean").read_text()
    assert "structure PackageCompatibilityProofSurfaceData" in text
    assert "structure PackageCompatibilityProofSurfaceObligations" in text
    assert "theorem PackageCompatibilityProofSurface" in text
    assert "PROOF_OBLIGATION_SURFACE_ONLY_NO_PACKAGE_COMPATIBILITY_PROOF" in text
