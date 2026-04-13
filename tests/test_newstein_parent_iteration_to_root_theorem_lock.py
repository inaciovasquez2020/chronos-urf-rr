from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_PARENT_ITERATION_TO_ROOT_THEOREM.md").read_text()
LEAN = Path("lean/Newstein/ParentIterationToRoot.lean").read_text()

def test_title_present():
    assert "# Newstein Parent-Iteration-to-Root Theorem" in DOC

def test_status_proved_present():
    assert "Status: PROVED" in DOC

def test_statement_present():
    assert "\\eta^R(v)=r." in DOC
    assert "\\eta_\\#^R=\\mathrm{Retr}_r." in DOC

def test_inputs_present():
    assert "TreeDepthMetricIdentity^thm" in DOC
    assert "MetricDepthCoincidence^thm" in DOC
    assert "ParentDepthDecrement^thm" in DOC

def test_role_present():
    assert "TreeContractionHomotopy^thm" in DOC

def test_theorem_decl_present():
    assert "theorem ParentIterationToRoot" in LEAN
