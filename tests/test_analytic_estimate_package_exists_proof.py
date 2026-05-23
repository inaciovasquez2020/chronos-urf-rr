import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_analytic_estimate_package_exists_proof_artifact_status():
    data = json.loads(
        (ROOT / "artifacts/chronos/analytic_estimate_package_exists_proof_2026_05_22.json").read_text()
    )
    assert data["status"] == "SYNTHETIC_INTERFACE_PROOF_CLOSED_GENUINE_PDE_PROOF_OPEN"
    assert data["repository"] == "chronos-urf-rr"
    assert data["next_admissible_object"] == "GENUINE_ANALYTIC_ESTIMATE_PACKAGE_EXISTS_PROOF"

def test_analytic_estimate_package_exists_proof_lean_surface():
    lean = (ROOT / "lean/Chronos/Frontier/AnalyticEstimatePackageExistsProof.lean").read_text()
    assert "def AnalyticEstimatePackageExists : Prop" in lean
    assert "axiom AnalyticEstimatePackageExists" not in lean
    assert "theorem analyticEstimatePackageExists_syntheticInterfaceProof" in lean
    assert "theorem bootstrapKernel_from_analyticEstimatePackageExists" in lean
    assert "theorem bootstrapKernel_from_syntheticAnalyticEstimatePackage" in lean
    assert "theorem collapseGate_from_analyticEstimatePackageExists" in lean
    assert "theorem collapseGate_from_syntheticAnalyticEstimatePackage" in lean

def test_analytic_estimate_package_exists_proof_boundaries():
    data = json.loads(
        (ROOT / "artifacts/chronos/analytic_estimate_package_exists_proof_2026_05_22.json").read_text()
    )
    doc = (ROOT / "docs/status/ANALYTIC_ESTIMATE_PACKAGE_EXISTS_PROOF_2026_05_22.md").read_text()
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
