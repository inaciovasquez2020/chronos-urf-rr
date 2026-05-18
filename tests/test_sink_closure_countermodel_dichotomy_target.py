import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/SinkClosureCountermodelDichotomyTarget.lean"
ARTIFACT = ROOT / "artifacts/chronos/sink_closure_countermodel_dichotomy_target_2026_05_18.json"
DOC = ROOT / "docs/status/SINK_CLOSURE_COUNTERMODEL_DICHOTOMY_TARGET_2026_05_18.md"

def test_dichotomy_target_status():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "OPEN_DICHOTOMY_TARGET_SURFACE_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False

def test_dichotomy_target_lean_surface():
    lean = LEAN.read_text()
    assert "structure SinkResolutionProblem" in lean
    assert "def CountermodelOrClosureDichotomyTarget" in lean
    assert "def CountermodelOrClosureDichotomyFailure" in lean
    assert "theorem unresolved_sink_excludes_dichotomy" in lean
    assert not re.search(r"\b(sorry|admit|axiom)\b", lean)

def test_dichotomy_target_artifact_surface():
    data = json.loads(ARTIFACT.read_text())
    assert "SinkResolutionProblem" in data["formal_objects"]
    assert "CountermodelOrClosureDichotomyTarget" in data["formal_objects"]
    assert "unresolved_sink_excludes_dichotomy" in data["proved_surface_theorems"]

def test_dichotomy_target_boundaries():
    doc = DOC.read_text()
    assert "Does not prove:" in doc
    assert "existence of closure certificates for every sink" in doc
    assert "existence of countermodel certificates for every sink" in doc
    assert "`CountermodelOrClosureDichotomyTarget`" in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "unrestricted Chronos-RR" in doc
    assert "unrestricted H4.1/FGL" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
