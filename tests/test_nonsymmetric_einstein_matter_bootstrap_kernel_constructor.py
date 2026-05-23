import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_constructor_artifact_status():
    data = json.loads(
        (
            ROOT
            / "artifacts/chronos/nonsymmetric_einstein_matter_bootstrap_kernel_constructor_2026_05_22.json"
        ).read_text()
    )
    assert data["status"] == "SUPPLIED_FIELD_CONSTRUCTOR_CLOSED_PDE_EXISTENCE_OPEN"
    assert data["repository"] == "chronos-urf-rr"
    assert data["next_admissible_object"] == "GENUINE_EINSTEIN_MATTER_PDE_FIELD_SUPPLY_THEOREM"

def test_constructor_lean_surface():
    lean = (
        ROOT / "lean/Chronos/Frontier/NonSymmetricEinsteinMatterBootstrapKernelConstructor.lean"
    ).read_text()
    assert "theorem nonSymmetricEinsteinMatterBootstrapKernel_constructor" in lean
    assert "theorem gravityClosureKernelTarget_from_supplied_fields" in lean
    assert "theorem collapseGate_from_supplied_bootstrap_fields" in lean
    assert "NonSymmetricEinsteinMatterBootstrapKernel D :=" in lean

def test_constructor_boundaries():
    data = json.loads(
        (
            ROOT
            / "artifacts/chronos/nonsymmetric_einstein_matter_bootstrap_kernel_constructor_2026_05_22.json"
        ).read_text()
    )
    doc = (
        ROOT / "docs/status/NONSYMMETRIC_EINSTEIN_MATTER_BOOTSTRAP_KERNEL_CONSTRUCTOR_2026_05_22.md"
    ).read_text()
    for token in [
        "unrestricted gravity closure",
        "cosmic censorship",
        "hoop conjecture",
        "four-dimensional collapse theorem",
        "unrestricted QL_CollapseGate",
        "unrestricted UniversalBoundaryCompactness",
        "Einstein-matter PDE existence",
        "Einstein-matter PDE regularity",
        "Einstein-matter PDE continuation",
        "Chronos-RR",
        "H4.1/FGL",
        "P vs NP",
        "any Clay problem",
    ]:
        assert token in data["does_not_prove"]
        assert token in doc
