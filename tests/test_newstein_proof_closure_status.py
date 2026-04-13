from pathlib import Path

def test_newstein_proof_closure_status_lock():
    s = Path("docs/status/NEWSTEIN_PROOF_CLOSURE_STATUS.md").read_text()
    assert "# Newstein Proof Closure Status" in s
    assert "## Solved" in s
    assert "## Locked frontier" in s


def test_newstein_reduction_frontier_sync() -> None:
    text = Path("docs/status/NEWSTEIN_PROOF_CLOSURE_STATUS.md").read_text(encoding="utf-8")
    assert "Reduction-complete." in text
    assert "OneStepParentDepthDecrement" in text
    assert "w \\neq r \\Longrightarrow d(\\eta(w),r)=d(w,r)-1" in text
    assert "Reduction-complete does not mean proof-complete." in text
