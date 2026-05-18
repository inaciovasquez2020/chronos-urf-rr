import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/FloorPreservingDomainLiftSufficientCondition.lean"
ARTIFACT = ROOT / "artifacts/chronos/floor_preserving_domain_lift_sufficient_condition_2026_05_18.json"
DOC = ROOT / "docs/status/FLOOR_PRESERVING_DOMAIN_LIFT_SUFFICIENT_CONDITION_2026_05_18.md"

def test_floor_preserving_lift_status():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "CONDITIONAL_LIFT_SUFFICIENT_CONDITION_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False

def test_floor_preserving_lift_lean_surface():
    lean = LEAN.read_text()
    assert "def FloorPreservingDomainLift" in lean
    assert "theorem floor_preserving_domain_lift_to_uniform_floor" in lean
    assert "theorem floor_preserving_domain_lift_to_admissible_lift" in lean
    assert "theorem floor_preserving_domain_lift_resolves_second_sink" in lean
    assert not re.search(r"\b(sorry|admit|axiom)\b", lean)

def test_floor_preserving_lift_artifact_surface():
    data = json.loads(ARTIFACT.read_text())
    assert "FloorPreservingDomainLift" in data["formal_objects"]
    assert "floor_preserving_domain_lift_to_admissible_lift" in data["proved_surface_theorems"]
    assert data["conditional_input"]["required_object"] == "FloorPreservingDomainLift"

def test_floor_preserving_lift_boundaries():
    doc = DOC.read_text()
    assert "Does not prove:" in doc
    assert "existence of `FloorPreservingDomainLift`" in doc
    assert "unconditional `FiniteSupportToAdmissibleDomainLift`" in doc
    assert "absence of `FiniteSupportLiftFailureCountermodel`" in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "unrestricted Chronos-RR" in doc
    assert "unrestricted H4.1/FGL" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
