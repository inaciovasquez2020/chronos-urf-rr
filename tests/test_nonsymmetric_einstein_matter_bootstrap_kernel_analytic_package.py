import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/nonsymmetric_einstein_matter_bootstrap_kernel_analytic_package_2026_05_22.json"
STATUS = ROOT / "docs/status/NONSYMMETRIC_EINSTEIN_MATTER_BOOTSTRAP_KERNEL_ANALYTIC_PACKAGE_2026_05_22.md"
LEAN = ROOT / "lean/Chronos/Frontier/NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage.lean"

def test_analytic_package_artifact_status():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "ANALYTIC_PACKAGE_INPUT_ONLY_NOT_PROVED"
    assert data["object"] == "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage"
    assert "NonSymmetricEinsteinMatterBootstrapKernelConstructorInput" in data["sufficient_for"]
    assert "NonSymmetricEinsteinMatterBootstrapKernelExistenceTarget" in data["sufficient_for"]

def test_analytic_package_remaining_objects():
    data = json.loads(ARTIFACT.read_text())
    assert data["remaining_missing_objects"] == [
        "analyticPackage",
        "pdeWellPosedness",
        "nonsymmetricEvolutionPersistence",
        "admissibilityPreservation",
        "concentrationTransport",
        "finiteTimeCollapseAlternative",
    ]

def test_analytic_package_status_doc_boundary():
    text = STATUS.read_text()
    assert "ANALYTIC_PACKAGE_INPUT_ONLY_NOT_PROVED" in text
    assert "∀ G : GenuineNonSymmetricEinsteinMatterPDEData" in text
    assert "This does not prove the analytic package." in text
    assert "This does not prove unrestricted cosmic censorship." in text
    assert "This does not prove any Clay problem." in text

def test_analytic_package_lean_surface_tokens():
    text = LEAN.read_text()
    for token in [
        "structure NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage",
        "def analytic_package_to_constructor_input",
        "theorem analytic_package_implies_constructor_input",
        "theorem analytic_package_implies_existence_target",
        "theorem analytic_package_closes_conditional_gravity_package",
        "theorem analytic_package_no_overclaim_boundary",
    ]:
        assert token in text
    words = text.replace("/", " ").replace("-", " ").replace("!", " ").split()
    assert "sorry" not in words
    assert "admit" not in words
    assert "axiom" not in words

def test_analytic_package_verifier_runs():
    subprocess.run(
        [sys.executable, "tools/verify_nonsymmetric_einstein_matter_bootstrap_kernel_analytic_package.py"],
        cwd=ROOT,
        check=True,
    )
