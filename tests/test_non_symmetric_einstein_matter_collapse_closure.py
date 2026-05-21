import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/non_symmetric_einstein_matter_collapse_closure_2026_05_20.json"
DOC = ROOT / "docs/status/NON_SYMMETRIC_EINSTEIN_MATTER_COLLAPSE_CLOSURE_2026_05_20.md"

def test_artifact_marks_macro_axiom_boundary_only():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "OPEN_PROBLEM_REQUIRED"
    assert data["classification"] == "MACRO_AXIOM_BOUNDARY_ONLY"
    assert data["minimal_missing_lemma"] == "NonSymmetricEinsteinMatterCollapseClosure"
    assert "UnrestrictedUniversalBoundaryCompactness" in data["components"]

def test_doc_preserves_no_overclaim_boundary():
    text = DOC.read_text()
    assert "Does not prove:" in text
    assert "unrestricted weak cosmic censorship" in text
    assert "unrestricted hoop theorem" in text
    assert "P vs NP" in text
    assert "any Clay problem" in text

def test_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_non_symmetric_einstein_matter_collapse_closure.py"],
        cwd=ROOT,
        check=True,
    )
