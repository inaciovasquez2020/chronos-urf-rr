from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_TREE_CONTRACTION_HOMOTOPY_PROOF_BLUEPRINT.md").read_text()

def test_title_present():
    assert "# Newstein Tree-Contraction Homotopy Proof Blueprint" in DOC

def test_status_open_present():
    assert "Status: OPEN" in DOC

def test_parent_map_present():
    assert "Define the parent map" in DOC
    assert "\\eta(v)=" in DOC

def test_prism_operator_present():
    assert "elementary prism operator" in DOC
    assert "\\partial \\phi + \\phi \\partial = \\mathrm{Id} - \\eta_\\#" in DOC

def test_summed_h_present():
    assert "h = \\sum_{j=0}^{R-1} \\eta_\\#^j \\circ \\phi" in DOC

def test_telescoping_present():
    assert "\\partial h + h \\partial" in DOC
    assert "\\mathrm{Id}-\\eta_\\#^R" in DOC

def test_retraction_step_present():
    assert "\\eta_\\#^R=\\mathrm{Retr}_r" in DOC
