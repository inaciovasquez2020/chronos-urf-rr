from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_TREE_CONTRACTION_HOMOTOPY_THEOREM.md").read_text()
LEAN = Path("lean/Newstein/TreeContractionHomotopy.lean").read_text()

def test_title_present():
    assert "# Newstein Tree-Contraction Homotopy Theorem" in DOC

def test_status_open_present():
    assert "Status: OPEN" in DOC

def test_inputs_present():
    assert "TreeDepthMetricIdentity^thm" in DOC
    assert "MetricDepthCoincidence^thm" in DOC
    assert "ParentDepthDecrement^thm" in DOC

def test_obligations_present():
    assert "tree_homotopy" in DOC
    assert "supp (tree_homotopy c) ⊆ B_R(r)" in DOC
    assert "∂ h + h ∂ = Id - Retr_r" in DOC

def test_dependency_chain_present():
    assert "TreeContractionHomotopy^thm => RootedBallTrivialization^thm => FiberQuotientRank^thm => DirectSumIndependence^thm => PerStepInformationBound^thm => QuotientGapClosure^unconditional" in DOC

def test_theorem_decl_present():
    assert "theorem TreeContractionHomotopy" in LEAN
