from pathlib import Path

def test_newstein_next_step_registry_lock():
    s = Path("docs/status/NEWSTEIN_NEXT_STEP_REGISTRY.md").read_text()
    assert "# Newstein Next-Step Registry" in s
    assert "## Solved" in s
    assert "## Locked frontier" in s


def test_newstein_next_step_registry_single_frontier() -> None:
    text = Path("docs/status/NEWSTEIN_NEXT_STEP_REGISTRY.md").read_text(encoding="utf-8")
    assert "Reduction-complete. Do not add new reduction locks." in text
    assert "## Single remaining frontier" in text
    assert "OneStepParentDepthDecrement" in text
    assert "w \\neq r \\Longrightarrow d(\\eta(w),r)=d(w,r)-1" in text
    assert "Replace the remaining frontier by a proof, not by another reduction note." in text

def test_newstein_next_step_registry_closure_state() -> None:
    text = Path("docs/status/NEWSTEIN_NEXT_STEP_REGISTRY.md").read_text(encoding="utf-8")
    assert "## Closure state" in text
    assert "Theorem-layer complete." in text
    assert "Do not add new reduction notes or frontier placeholders for the completed Newstein chain." in text
