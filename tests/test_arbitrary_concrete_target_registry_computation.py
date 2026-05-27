import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/ArbitraryConcreteTargetRegistryComputation.lean"
ART = ROOT / "artifacts/chronos/arbitrary_concrete_target_registry_computation_2026_05_27.json"
DOC = ROOT / "docs/status/ARBITRARY_CONCRETE_TARGET_REGISTRY_COMPUTATION_2026_05_27.md"


def test_lean_surface_defines_required_objects():
    text = LEAN.read_text()
    assert "structure ConcreteTargetRegistry" in text
    assert "structure FiniteConcreteTargetRegistry" in text
    assert "structure OneRegistrySemanticComputation" in text
    assert "structure ArbitraryFiniteConcreteRegistryComputation" in text
    assert "def one_registry_computation_lifts_to_arbitrary_finite_concrete_target_registries" in text


def test_artifact_boundary_lock():
    data = json.loads(ART.read_text())
    assert data["status"] == "FINITE_CONCRETE_TARGET_REGISTRY_COMPUTATION_LIFT_CLOSED_WITNESS_ONLY"
    assert "unrestricted semantic-rank-to-fiber-entropy bridge" in data["does_not_prove"]
    assert "UniversalFiberEntropyGap" in data["does_not_prove"]
    assert "Chronos-RR" in data["does_not_prove"]
    assert "H4.1/FGL" in data["does_not_prove"]
    assert "P vs NP" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]


def test_status_doc_contains_weakest_missing_ingredient():
    text = DOC.read_text()
    assert "construct canonical one-registry semantic computation witnesses" in text
    assert "Does not prove:" in text
