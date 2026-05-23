import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_genuine_reduction_artifact_status():
    data = json.loads(
        (ROOT / "artifacts/chronos/genuine_analytic_estimate_package_proof_reduction_2026_05_22.json").read_text()
    )
    assert data["status"] == "GENUINE_PDE_WITNESS_REDUCTION_CLOSED_GENUINE_PDE_WITNESS_OPEN"
    assert data["repository"] == "chronos-urf-rr"
    assert data["next_admissible_object"] == "GENUINE_PDE_ESTIMATE_WITNESS"

def test_genuine_reduction_lean_surface():
    lean = (ROOT / "lean/Chronos/Frontier/GenuineAnalyticEstimatePackageProofReduction.lean").read_text()
    assert "structure GenuineEinsteinMatterDatum" in lean
    assert "structure GenuinePDEEstimateWitness" in lean
    assert "def analyticEstimatePackage_from_genuinePDEEstimateWitness" in lean
    assert "theorem analyticEstimatePackageExists_from_genuinePDEEstimateWitness" in lean
    assert "theorem bootstrapKernel_from_genuinePDEEstimateWitness" in lean
    assert "theorem collapseGate_from_genuinePDEEstimateWitness" in lean
    assert "def GenuineAnalyticEstimatePackageExistsProof : Prop" in lean
    assert "theorem analyticEstimatePackageExists_from_genuineProof" in lean
    assert "axiom " not in lean

def test_genuine_reduction_boundaries():
    data = json.loads(
        (ROOT / "artifacts/chronos/genuine_analytic_estimate_package_proof_reduction_2026_05_22.json").read_text()
    )
    doc = (ROOT / "docs/status/GENUINE_ANALYTIC_ESTIMATE_PACKAGE_PROOF_REDUCTION_2026_05_22.md").read_text()
    for token in [
        "genuine Einstein-matter PDE existence",
        "genuine Einstein-matter PDE regularity",
        "genuine Einstein-matter PDE continuation",
        "unconditional gravity closure",
        "unrestricted gravity closure",
        "cosmic censorship",
        "hoop conjecture",
        "four-dimensional collapse theorem",
        "unrestricted QL_CollapseGate",
        "unrestricted UniversalBoundaryCompactness",
        "Chronos-RR",
        "H4.1/FGL",
        "P vs NP",
        "any Clay problem",
    ]:
        assert token in data["does_not_prove"]
        assert token in doc
