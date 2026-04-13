from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_PARENT_ITERATION_DEPTH_FORMULA_THEOREM.md").read_text(encoding="utf-8")

def test_title_present():
    assert "# Newstein Parent Iteration Depth Formula Theorem" in DOC

def test_status_proved_present():
    assert "Status: PROVED" in DOC

def test_statement_present():
    assert r"d\!\left(\eta^{\,n}(v), r\right)=d(v,r)-n" in DOC

def test_inputs_present():
    assert "one-step parent-depth decrement law" in DOC

def test_role_present():
    assert r"\eta^{\,d(v,r)}(v)=r" in DOC
