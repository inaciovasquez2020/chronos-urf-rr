import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/FiniteSupportToAdmissibleDomainLiftTarget.lean"
ARTIFACT = ROOT / "artifacts/chronos/finite_support_to_admissible_domain_lift_target_2026_05_18.json"
DOC = ROOT / "docs/status/FINITE_SUPPORT_TO_ADMISSIBLE_DOMAIN_LIFT_TARGET_2026_05_18.md"

def test_lift_target_status():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "OPEN_LIFT_TARGET_SURFACE_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False

def test_lift_target_lean_surface():
    lean = LEAN.read_text()
    assert "def FiniteSupportToAdmissibleDomainLift" in lean
    assert "def FiniteSupportLiftFailureCountermodel" in lean
    assert "theorem finite_support_lift_transfers_floor" in lean
    assert "theorem finite_support_lift_failure_countermodel_excludes_lift" in lean
    assert not re.search(r"\b(sorry|admit|axiom)\b", lean)

def test_lift_target_artifact_surface():
    data = json.loads(ARTIFACT.read_text())
    assert "FiniteSupportToAdmissibleDomainLift" in data["formal_objects"]
    assert "FiniteSupportLiftFailureCountermodel" in data["formal_objects"]
    assert "finite_support_lift_resolves_admissible_sink" in data["proved_surface_theorems"]

def test_lift_target_boundaries():
    doc = DOC.read_text()
    assert "Does not prove:" in doc
    assert "existence of `FiniteSupportToAdmissibleDomainLift`" in doc
    assert "absence of `FiniteSupportLiftFailureCountermodel`" in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "unrestricted Chronos-RR" in doc
    assert "unrestricted H4.1/FGL" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
