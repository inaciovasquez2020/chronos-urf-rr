import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/FiniteSupportUniformFloorToTarget.lean"
ARTIFACT = ROOT / "artifacts/chronos/finite_support_uniform_floor_to_target_2026_05_18.json"
DOC = ROOT / "docs/status/FINITE_SUPPORT_UNIFORM_FLOOR_TO_TARGET_2026_05_18.md"

def test_finite_support_uniform_floor_status():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "FINITE_SUPPORT_TARGET_CLOSURE_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False

def test_finite_support_uniform_floor_lean_surface():
    lean = LEAN.read_text()
    assert "def FiniteSupportUniformFloorCertificate" in lean
    assert "theorem finite_support_uniform_floor_to_target" in lean
    assert "theorem finite_support_uniform_floor_resolves_sink" in lean
    assert not re.search(r"\b(sorry|admit|axiom)\b", lean)

def test_finite_support_uniform_floor_artifact_surface():
    data = json.loads(ARTIFACT.read_text())
    assert "FiniteSupportUniformFloorCertificate" in data["formal_objects"]
    assert "finite_support_uniform_floor_to_target" in data["proved_surface_theorems"]
    assert "finite_support_uniform_floor_resolves_sink" in data["proved_surface_theorems"]

def test_finite_support_uniform_floor_boundaries():
    doc = DOC.read_text()
    assert "Does not prove:" in doc
    assert "finite-support-to-admissible-domain lift" in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "unrestricted Chronos-RR" in doc
    assert "unrestricted H4.1/FGL" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
