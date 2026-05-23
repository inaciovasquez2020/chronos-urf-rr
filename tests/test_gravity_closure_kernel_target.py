import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_gravity_closure_kernel_target_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/gravity_closure_kernel_target_2026_05_22.json").read_text()
    )
    assert data["status"] == "KERNEL_TARGET_ONLY_GRAVITY_CLOSURE_OPEN"
    assert data["repository"] == "chronos-urf-rr"
    assert data["closed_result"] == "collapseGate_from_bootstrapKernel"
    assert data["open_target"] == "GravityClosureKernelTarget"
    assert "NonSymmetricEinsteinMatterBootstrapKernel" in data["missing_object"]

def test_gravity_closure_kernel_target_lean_surface():
    lean = (ROOT / "lean/Chronos/Frontier/GravityClosureKernelTarget.lean").read_text()
    assert "structure FourDimensionalNonSymmetricEinsteinMatterData" in lean
    assert "structure NonSymmetricEinsteinMatterBootstrapKernel" in lean
    assert "theorem collapseGate_from_bootstrapKernel" in lean
    assert "def GravityClosureKernelTarget : Prop" in lean
    assert "sourceLevelEvidence_does_not_construct_kernel" in lean

def test_gravity_closure_kernel_target_boundaries():
    data = json.loads(
        (ROOT / "artifacts/chronos/gravity_closure_kernel_target_2026_05_22.json").read_text()
    )
    doc = (ROOT / "docs/status/GRAVITY_CLOSURE_KERNEL_TARGET_2026_05_22.md").read_text()
    for token in [
        "gravity closure",
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
