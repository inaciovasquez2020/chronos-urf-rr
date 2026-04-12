from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_METRIC_DEPTH_COINCIDENCE_LEMMA.md").read_text()
LEAN = Path("lean/Newstein/MetricDepthCoincidence.lean").read_text()

def test_status_proved_present():
    assert "Status: PROVED" in DOC

def test_typed_bfs_bridge_present():
    assert "structure HasBFSDistEqGraphDist" in LEAN
    assert "bfs_dist_eq_graph_dist" in LEAN

def test_tree_identity_used():
    assert "rw [TreeDepthMetricIdentity hT x]" in LEAN

def test_metric_depth_coincidence_present():
    assert "theorem MetricDepthCoincidence" in LEAN
    assert "depth_G x = d_T root_G x" in LEAN

def test_doc_discharge_present():
    assert "## Discharge" in DOC
    assert "TreeDepthMetricIdentity" in DOC
    assert "bfs_dist_eq_graph_dist" in DOC

def test_dependency_chain_present():
    assert "MetricDepthCoincidence^proved => ParentDepthDecrement^conditional => RootedBallTrivialization^conditional => FiberQuotientRank^conditional => DirectSumIndependence^conditional => PerStepInformationBound^conditional => QuotientGapClosure^conditional" in DOC
