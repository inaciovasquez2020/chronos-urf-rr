import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/UniformPositiveFiberMassFloorTarget.lean"
ARTIFACT = ROOT / "artifacts/chronos/uniform_positive_fiber_mass_floor_target_2026_05_18.json"
DOC = ROOT / "docs/status/UNIFORM_POSITIVE_FIBER_MASS_FLOOR_TARGET_2026_05_18.md"

def test_uniform_positive_target_status():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "OPEN_TARGET_SURFACE_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False

def test_uniform_positive_target_lean_objects_present():
    lean = LEAN.read_text()
    assert "def UniformPositiveFiberMassFloor" in lean
    assert "def NoUniformPositiveFiberMassFloorCountermodel" in lean
    assert "inductive UniformPositiveFiberMassSinkResolution" in lean
    assert "theorem countermodel_excludes_uniform_positive_floor" in lean

def test_uniform_positive_target_has_no_holes():
    lean = LEAN.read_text()
    assert not re.search(r"\b(sorry|admit|axiom)\b", lean)

def test_uniform_positive_target_boundary_doc():
    doc = DOC.read_text()
    assert "Does not prove:" in doc
    assert "existence of `UniformPositiveFiberMassFloor`" in doc
    assert "absence of `NoUniformPositiveFiberMassFloorCountermodel`" in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "unrestricted Chronos-RR" in doc
    assert "unrestricted H4.1/FGL" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc

def test_uniform_positive_target_countermodel_is_refutation_schema():
    data = json.loads(ARTIFACT.read_text())
    assert data["target_countermodel_exit"]["required_object"] == "NoUniformPositiveFiberMassFloorCountermodel"
    assert "countermodel_excludes_uniform_positive_floor" in data["proved_surface_theorems"]
