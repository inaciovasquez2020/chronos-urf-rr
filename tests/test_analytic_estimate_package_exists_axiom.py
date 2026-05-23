import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_axiom_artifact_status():
    data = json.loads(
        (ROOT / "artifacts/chronos/analytic_estimate_package_exists_axiom_2026_05_22.json").read_text()
    )
    assert data["status"] == "CONDITIONAL_ANALYTIC_PACKAGE_EXISTENCE_REDUCTION_ONLY_NO_UNCONDITIONAL_GRAVITY_PROOF"
    assert data["proposition"] == "AnalyticEstimatePackageExists"
    assert data["next_admissible_object"] == "ANALYTIC_ESTIMATE_PACKAGE_EXISTS_PROOF"

def test_axiom_lean_surface():
    lean = (ROOT / "lean/Chronos/Frontier/AnalyticEstimatePackageExistsAxiom.lean").read_text()
    assert "structure ToolkitAdmissibleRegion" in lean
    assert "structure AnalyticEstimatePackage" in lean
    assert "def AnalyticEstimatePackageExists : Prop" in lean
    assert "axiom AnalyticEstimatePackageExists" not in lean
    assert "theorem bootstrapKernel_from_analyticEstimatePackageExists" in lean
    assert "theorem collapseGate_from_analyticEstimatePackageExists" in lean

def test_axiom_boundaries():
    data = json.loads(
        (ROOT / "artifacts/chronos/analytic_estimate_package_exists_axiom_2026_05_22.json").read_text()
    )
    doc = (ROOT / "docs/status/ANALYTIC_ESTIMATE_PACKAGE_EXISTS_AXIOM_2026_05_22.md").read_text()
    for token in [
        "unconditional gravity closure",
        "unrestricted gravity closure",
        "cosmic censorship",
        "hoop conjecture",
        "four-dimensional collapse theorem",
        "unrestricted QL_CollapseGate",
        "unrestricted UniversalBoundaryCompactness",
        "unaxiomatized Einstein-matter PDE existence",
        "unaxiomatized Einstein-matter PDE regularity",
        "unaxiomatized Einstein-matter PDE continuation",
        "Chronos-RR",
        "H4.1/FGL",
        "P vs NP",
        "any Clay problem",
    ]:
        assert token in data["does_not_prove"]
        assert token in doc
