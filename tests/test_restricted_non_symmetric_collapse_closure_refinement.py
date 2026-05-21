import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/restricted_non_symmetric_collapse_closure_refinement_2026_05_21.json"
DOC = ROOT / "docs/status/RESTRICTED_NON_SYMMETRIC_COLLAPSE_CLOSURE_REFINEMENT_2026_05_21.md"

def test_refinement_target_is_strict_and_restricted():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "STRICT_REFINEMENT_TARGET_OPEN"
    assert data["classification"] == "RESTRICTED_REFINEMENT_TARGET_ONLY"
    assert data["parent_macro_axiom"] == "NonSymmetricEinsteinMatterCollapseClosure"
    assert data["restricted_refinement_target"] == "RestrictedNonSymmetricCollapseClosure"
    assert "RestrictedCollapseDomain D" in data["restriction_parameters"]
    assert "RestrictedCollapseSurface S" in data["restriction_parameters"]

def test_corrected_obstruction_is_scope_mismatch_not_contradiction():
    data = json.loads(ARTIFACT.read_text())
    obstruction = data["corrected_obstruction"]
    assert "not logically contradictory" in obstruction
    assert "scope mismatch" in obstruction

def test_boundary_preserves_no_unrestricted_claims():
    text = DOC.read_text()
    assert "Does not prove:" in text
    assert "NonSymmetricEinsteinMatterCollapseClosure" in text
    assert "unrestricted universal boundary compactness" in text
    assert "unrestricted QL-collapse gating" in text
    assert "unrestricted weak cosmic censorship" in text
    assert "unrestricted hoop theorem" in text
    assert "P vs NP" in text
    assert "any Clay problem" in text

def test_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_restricted_non_symmetric_collapse_closure_refinement.py"],
        cwd=ROOT,
        check=True,
    )
