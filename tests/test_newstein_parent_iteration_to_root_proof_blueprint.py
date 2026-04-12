from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_PARENT_ITERATION_TO_ROOT_PROOF_BLUEPRINT.md").read_text()

def test_title_present():
    assert "# Newstein Parent-Iteration-to-Root Proof Blueprint" in DOC

def test_status_open_present():
    assert "Status: OPEN" in DOC

def test_objective_present():
    assert "\\eta^R(v)=r," in DOC
    assert "\\eta_\\#^R=\\mathrm{Retr}_r." in DOC

def test_inputs_present():
    assert "TreeDepthMetricIdentity^thm" in DOC
    assert "MetricDepthCoincidence^thm" in DOC
    assert "ParentDepthDecrement^thm" in DOC

def test_depth_descent_present():
    assert "d(\\eta(v))=d(v)-1." in DOC

def test_induction_formula_present():
    assert "d(\\eta^j(v))=\\max(d(v)-j,0)." in DOC

def test_chain_role_present():
    assert "\\mathrm{ParentIterationToRoot}^\\mathrm{thm}" in DOC
    assert "\\mathrm{TreeContractionHomotopy}^\\mathrm{thm}" in DOC
