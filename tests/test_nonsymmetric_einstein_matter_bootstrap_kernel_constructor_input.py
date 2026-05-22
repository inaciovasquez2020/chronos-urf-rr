import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/nonsymmetric_einstein_matter_bootstrap_kernel_constructor_input_2026_05_22.json"
STATUS = ROOT / "docs/status/NONSYMMETRIC_EINSTEIN_MATTER_BOOTSTRAP_KERNEL_CONSTRUCTOR_INPUT_2026_05_22.md"
LEAN = ROOT / "lean/Chronos/Frontier/NonSymmetricEinsteinMatterBootstrapKernelConstructorInput.lean"

def test_constructor_input_artifact_status_and_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "CONSTRUCTOR_INPUT_ONLY_TARGET_REDUCED_NOT_SOLVED"
    assert data["object"] == "NonSymmetricEinsteinMatterBootstrapKernelConstructorInput"
    assert data["reduces_target"] == "NonSymmetricEinsteinMatterBootstrapKernelExistenceTarget"
    for token in [
        "unrestricted cosmic censorship",
        "unrestricted hoop theorem",
        "unrestricted QL_CollapseGate",
        "unrestricted UniversalBoundaryCompactness",
        "P vs NP",
        "any Clay problem",
    ]:
        assert token in data["does_not_prove"]

def test_constructor_input_remaining_objects_are_exact():
    data = json.loads(ARTIFACT.read_text())
    assert data["remaining_missing_objects"] == [
        "pdeEvolution",
        "nonsymmetricEvolution",
        "initialAdmissible",
        "surfaceRealization",
        "concentrationTransport",
        "finiteTimeCollapseAlternative",
    ]

def test_constructor_input_status_doc_records_boundary():
    text = STATUS.read_text()
    assert "CONSTRUCTOR_INPUT_ONLY_TARGET_REDUCED_NOT_SOLVED" in text
    assert "NonSymmetricEinsteinMatterBootstrapKernelExistenceTarget" in text
    assert "This does not prove unrestricted cosmic censorship." in text
    assert "This does not prove any Clay problem." in text

def test_constructor_input_lean_surface_tokens():
    text = LEAN.read_text()
    for token in [
        "structure NonSymmetricEinsteinMatterBootstrapKernelConstructorInput",
        "def kernel_from_constructor_input",
        "theorem constructor_input_implies_existence_target",
        "theorem constructor_input_closes_conditional_gravity_package",
        "theorem constructor_input_no_overclaim_boundary",
    ]:
        assert token in text
    words = text.replace("/", " ").replace("-", " ").replace("!", " ").split()
    assert "sorry" not in words
    assert "admit" not in words
    assert "axiom" not in words

def test_constructor_input_verifier_runs():
    subprocess.run(
        [sys.executable, "tools/verify_nonsymmetric_einstein_matter_bootstrap_kernel_constructor_input.py"],
        cwd=ROOT,
        check=True,
    )
