from pathlib import Path

LEAN = Path("lean/Newstein/TreeDepthMetricIdentity.lean").read_text()
DOC = Path("docs/math/NEWSTEIN_TREE_DEPTH_METRIC_IDENTITY.md").read_text()

def test_parent_iter_present():
    assert "def parentIter" in LEAN
    assert "parent_eventually_root" in LEAN

def test_no_sorry():
    assert "sorry" not in LEAN

def test_theorem_present():
    assert "theorem TreeDepthMetricIdentity" in LEAN
    assert "induction n generalizing x" in LEAN

def test_doc_status_proved():
    assert "Status: PROVED" in DOC

def test_doc_statement_present():
    assert r"\forall x,\ \operatorname{depth}_G(x)=d_G(r,x)." in DOC
    assert r"\forall x,\ \exists n,\ p^{[n]}(x)=r\)." in DOC

def test_dependency_present():
    assert "TreeDepthMetricIdentity^proved => MetricDepthCoincidence^conditional => ParentDepthDecrement^conditional => RootedBallTrivialization^conditional => FiberQuotientRank^conditional => DirectSumIndependence^conditional => PerStepInformationBound^conditional => QuotientGapClosure^conditional" in DOC
