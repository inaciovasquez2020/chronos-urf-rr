from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_PARENT_ITERATION_DEPTH_FORMULA_THEOREM.md").read_text()
LEAN = Path("lean/Newstein/ParentIterationDepthFormula.lean").read_text()

def test_title_present():
    assert "# Newstein Parent-Iteration Depth Formula Theorem" in DOC

def test_status_open_present():
    assert "Status: OPEN" in DOC

def test_statement_present():
    assert "d(\\eta^j(v))=\\max(d(v)-j,0)." in DOC

def test_inputs_present():
    assert "MetricDepthCoincidence^thm" in DOC
    assert "ParentDepthDecrement^thm" in DOC

def test_role_present():
    assert "\\eta^R(v)=r" in DOC
    assert "\\eta_\\#^R=\\mathrm{Retr}_r." in DOC

def test_theorem_decl_present():
    assert "theorem ParentIterationDepthFormula" in LEAN
