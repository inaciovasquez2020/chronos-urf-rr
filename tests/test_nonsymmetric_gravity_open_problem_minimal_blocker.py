import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/nonsymmetric_gravity_open_problem_minimal_blocker_2026_05_22.json"
STATUS = ROOT / "docs/status/NONSYMMETRIC_GRAVITY_OPEN_PROBLEM_MINIMAL_BLOCKER_2026_05_22.md"
LEAN = ROOT / "lean/Chronos/Frontier/NonSymmetricGravityOpenProblemMinimalBlocker.lean"

FIELDS = [
    "pdeEvolution",
    "nonsymmetricEvolution",
    "initialAdmissible",
    "surfaceRealization",
    "concentrationTransport",
    "finiteTimeCollapseAlternative",
]

def test_minimal_blocker_status_and_problem():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "OPEN_PROBLEM_FRONTIER_C_MINIMAL_BLOCKER"
    assert "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage G" in data["problem"]
    assert data["weakest_sufficient_object"] == "SixFieldAnalyticPackageHypothesis"

def test_single_field_claim_is_rejected():
    data = json.loads(ARTIFACT.read_text())
    assert data["corrected_false_claim"] == "A single uniform field does not close the six-field analytic package."
    assert data["single_fields_not_sufficient_alone"] == FIELDS

def test_required_fields_are_exact():
    data = json.loads(ARTIFACT.read_text())
    assert data["required_fields"] == FIELDS

def test_status_doc_boundary():
    text = STATUS.read_text()
    assert "OPEN_PROBLEM_FRONTIER_C_MINIMAL_BLOCKER" in text
    assert "Any one field, proved uniformly, unblocks all six" in text
    assert "is false" in text
    assert "This does not prove any single field implies the other five fields." in text
    assert "This does not prove any Clay problem." in text

def test_lean_surface_no_sorry_axiom_admit():
    text = LEAN.read_text()
    for token in [
        "def openProblem : Prop",
        "structure SixFieldAnalyticPackageHypothesis",
        "theorem six_field_hypothesis_closes_open_problem",
        "theorem open_problem_minimal_blocker_no_overclaim_boundary",
    ]:
        assert token in text
    words = text.replace("/", " ").replace("-", " ").replace("!", " ").split()
    assert "sorry" not in words
    assert "admit" not in words
    assert "axiom" not in words

def test_verifier_runs():
    subprocess.run(
        [sys.executable, "tools/verify_nonsymmetric_gravity_open_problem_minimal_blocker.py"],
        cwd=ROOT,
        check=True,
    )
