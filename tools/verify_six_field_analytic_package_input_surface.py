from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/SixFieldAnalyticPackageInputSurface.lean"
ARTIFACT = ROOT / "artifacts/chronos/six_field_analytic_package_input_surface_2026_05_23.json"
STATUS = ROOT / "docs/status/SIX_FIELD_ANALYTIC_PACKAGE_INPUT_SURFACE_2026_05_23.md"

REQUIRED_LEAN = [
    "structure EinsteinMatterPDEModel",
    "structure GaugeFixing",
    "structure InitialDataClass",
    "structure EnergyFunctional",
    "structure BootstrapEnergyCloses",
    "structure SixFieldAnalyticPackageInputSurface",
    "theorem SixFieldAnalyticPackageInputSurface.has_bootstrap_closure",
]

FORBIDDEN_PROMOTIONS = [
    "Status: THEOREM_PROVED",
    "Status: CLOSED",
    "SixFieldAnalyticPackageHypothesis proved",
    "cosmic censorship proved",
    "hoop conjecture proved",
    "P vs NP proved",
    "Clay problem solved",
]

def main() -> None:
    assert LEAN.exists(), f"missing {LEAN}"
    assert ARTIFACT.exists(), f"missing {ARTIFACT}"
    assert STATUS.exists(), f"missing {STATUS}"

    lean = LEAN.read_text()
    status = STATUS.read_text()
    data = json.loads(ARTIFACT.read_text())

    for token in REQUIRED_LEAN:
        assert token in lean, token

    assert data["status"] == "INPUT_SURFACE_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["next_missing_object"] == "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage"

    for obj in [
        "EinsteinMatterPDEModel",
        "GaugeFixing",
        "InitialDataClass",
        "EnergyFunctional",
        "BootstrapEnergyCloses",
    ]:
        assert obj in data["objects_defined"], obj
        assert obj in status, obj

    for boundary in [
        "SixFieldAnalyticPackageHypothesis",
        "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage",
        "gravity closure",
        "Chronos-RR",
        "H4.1/FGL",
        "P vs NP",
        "any Clay problem",
    ]:
        assert boundary in status, boundary
        assert any(boundary in item for item in data["does_not_prove"]), boundary

    combined = lean + "\n" + status + "\n" + ARTIFACT.read_text()
    for forbidden in FORBIDDEN_PROMOTIONS:
        assert forbidden not in combined, forbidden

    print("Six-field analytic package input surface verification OK.")
    print("Status:", data["status"])
    print("Next missing object:", data["next_missing_object"])

if __name__ == "__main__":
    main()
