from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_PARENT_ITERATION_DEPTH_FORMULA_PROOF_BLUEPRINT.md").read_text()

def test_title_present():
    assert "# Newstein Parent-Iteration Depth Formula Proof Blueprint" in DOC

def test_status_open_present():
    assert "Status: OPEN" in DOC

def test_objective_present():
    assert "d(\\eta^j(v))=\\max(d(v)-j,0)." in DOC

def test_base_case_present():
    assert "d(\\eta^0(v))=d(v)=\\max(d(v)-0,0)." in DOC

def test_case_split_present():
    assert "### Case 1" in DOC
    assert "### Case 2" in DOC

def test_decrement_step_present():
    assert "d(\\eta^{j+1}(v))=d(\\eta^j(v))-1=d(v)-(j+1)." in DOC

def test_role_present():
    assert "\\eta^R(v)=r," in DOC
    assert "ParentIterationToRoot^thm" in DOC
