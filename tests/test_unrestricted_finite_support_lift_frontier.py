import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/UnrestrictedFiniteSupportLiftFrontier.lean"
ARTIFACT = ROOT / "artifacts/chronos/unrestricted_finite_support_lift_frontier_2026_05_18.json"
DOC = ROOT / "docs/status/UNRESTRICTED_FINITE_SUPPORT_LIFT_FRONTIER_2026_05_18.md"

def test_unrestricted_lift_frontier_status():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "UNRESTRICTED_LIFT_FRONTIER_OPEN"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False

def test_unrestricted_lift_frontier_lean_surface():
    lean = LEAN.read_text()
    assert "def UnrestrictedFiniteSupportToAdmissibleDomainLift" in lean
    assert "def UnrestrictedFiniteSupportLiftFailureCountermodel" in lean
    assert "theorem unrestricted_lift_transfers_any_finite_floor" in lean
    assert not re.search(r"\b(sorry|admit|axiom)\b", lean)

def test_unrestricted_lift_frontier_boundary():
    doc = DOC.read_text()
    assert "Does not prove:" in doc
    assert "`UnrestrictedFiniteSupportToAdmissibleDomainLift`" in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "unrestricted Chronos-RR" in doc
    assert "unrestricted H4.1/FGL" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
