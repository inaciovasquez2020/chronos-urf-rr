import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_closeout_stack_status_and_next_build():
    data = json.loads((ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_closeout_stack_2026_05_23.json").read_text())
    assert data["status"] == "BUILD_CLOSEOUT_SURFACE_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["previous_object"] == "RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF"
    assert data["next_build_status"] == "NEXT_BUILD_ALLOWED_AFTER_STOP_LOCK"

def test_closeout_stack_records_all_remaining_objects():
    data = json.loads((ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_closeout_stack_2026_05_23.json").read_text())
    assert data["remaining_next_admissible_objects_closed_as_surfaces"] == [
        "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
        "PACKAGE_COMPATIBILITY_PROOF",
        "TARGET_INTERFACE_COMPATIBILITY_PROOF",
        "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF",
        "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_BUILD_STOP_LOCK",
    ]

def test_closeout_stack_boundaries_are_preserved():
    data = json.loads((ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_closeout_stack_2026_05_23.json").read_text())
    for token in [
        "no analytic derivation of the local balance law",
        "no unconditional restricted concentration monotonicity theorem",
        "no unconditional restricted continuation norm theorem",
        "no analytic Einstein-matter bootstrap package",
        "no concrete analytic Einstein-matter estimate package proof",
        "no threshold crossing proof",
        "no gravity closure",
        "no Chronos-RR",
        "no H4.1/FGL",
        "no P vs NP",
        "no Clay problem",
    ]:
        assert token in data["boundary"]

def test_closeout_stack_lean_surface_terms():
    text = (ROOT / "lean/Chronos/Frontier/ConcreteAnalyticEinsteinMatterEstimatePackageCloseoutStack.lean").read_text()
    for token in [
        "RestrictedContinuationNormControlProof",
        "PackageCompatibilityProof",
        "TargetInterfaceCompatibilityProof",
        "ConcreteAnalyticEinsteinMatterEstimatePackageProof",
        "ConcreteAnalyticEinsteinMatterEstimatePackageBuildStopLock",
    ]:
        assert token in text
