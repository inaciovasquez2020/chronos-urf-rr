from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_PARENT_ITERATION_TO_ROOT_THEOREM.md").read_text()
BLUEPRINT = Path("docs/math/NEWSTEIN_PARENT_ITERATION_TO_ROOT_PROOF_BLUEPRINT.md").read_text()
REGISTRY = Path("docs/status/NEWSTEIN_NEXT_STEP_REGISTRY.md").read_text()
LEAN = Path("lean/Newstein/ParentIterationToRoot.lean").read_text()

def test_registry_marks_parent_iteration_to_root_as_frontier():
    assert "ParentIterationToRoot^thm" in REGISTRY

def test_theorem_target_present():
    assert "# Newstein Parent-Iteration-to-Root Theorem" in DOC
    assert "Status: OPEN" in DOC
    assert "\\eta^R(v)=r." in DOC
    assert "\\eta_\\#^R=\\mathrm{Retr}_r." in DOC

def test_blueprint_present():
    assert "# Newstein Parent-Iteration-to-Root Proof Blueprint" in BLUEPRINT
    assert "d(\\eta(v))=d(v)-1." in BLUEPRINT
    assert "d(\\eta^j(v))=\\max(d(v)-j,0)." in BLUEPRINT

def test_placeholder_theorem_decl_still_explicit():
    assert "theorem ParentIterationToRoot" in LEAN
