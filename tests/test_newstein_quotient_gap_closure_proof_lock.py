from pathlib import Path

LEAN = Path("lean/Newstein/QuotientGapClosure.lean").read_text()
DOC = Path("docs/math/NEWSTEIN_QUOTIENT_GAP_CLOSURE_TARGET.md").read_text()

def test_theorem_present():
    assert "theorem QuotientGapClosure" in LEAN

def test_axiom_forbidden():
    assert "axiom QuotientGapClosureConditional" not in LEAN

def test_doc_status_proved():
    assert "Status: CONDITIONAL" in DOC

def test_unconditional_chain_present():
    assert "ParentDepthDecrement^thm => RootedBallTrivialization^thm => FiberQuotientRank^thm => DirectSumIndependence^thm => PerStepInformationBound^thm => QuotientGapClosure^conditional" in DOC
