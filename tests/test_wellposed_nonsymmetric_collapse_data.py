import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/wellposed_nonsymmetric_collapse_data_2026_05_22.json"
STATUS = ROOT / "docs/status/WELLPPOSED_NONSYMMETRIC_COLLAPSE_DATA_2026_05_22.md"
LEAN = ROOT / "lean/Chronos/Frontier/WellPosedNonSymmetricCollapseData.lean"

def test_restricted_package_artifact_status():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "RESTRICTED_PACKAGE_THEOREM_ONLY"
    assert data["object"] == "WellPosedNonSymmetricCollapseData"
    assert data["assumed_field"] == "closure : NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage base"

def test_restricted_theorems_recorded():
    data = json.loads(ARTIFACT.read_text())
    assert data["restricted_theorems"] == [
        "restricted_analytic_package",
        "restricted_constructor_input",
        "restricted_existence_target",
        "restricted_package_no_overclaim_boundary",
    ]

def test_status_doc_boundary():
    text = STATUS.read_text()
    assert "RESTRICTED_PACKAGE_THEOREM_ONLY" in text
    assert "This does not prove SixFieldAnalyticPackageHypothesis." in text
    assert "This does not prove the unrestricted analytic package." in text
    assert "This does not prove any Clay problem." in text

def test_lean_surface_no_sorry_axiom_admit():
    text = LEAN.read_text()
    for token in [
        "structure WellPosedNonSymmetricCollapseData",
        "theorem restricted_analytic_package",
        "theorem restricted_constructor_input",
        "theorem restricted_existence_target",
        "theorem restricted_package_no_overclaim_boundary",
    ]:
        assert token in text
    words = text.replace("/", " ").replace("-", " ").replace("!", " ").split()
    assert "sorry" not in words
    assert "admit" not in words
    assert "axiom" not in words

def test_verifier_runs():
    subprocess.run(
        [sys.executable, "tools/verify_wellposed_nonsymmetric_collapse_data.py"],
        cwd=ROOT,
        check=True,
    )
