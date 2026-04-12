from pathlib import Path

def test_newstein_per_step_information_bound_lock():
    s = Path("docs/math/NEWSTEIN_PER_STEP_INFORMATION_BOUND.md").read_text()
    assert "# Newstein Per-Step Information Bound" in s
    assert "## Status\nOPEN" in s
    assert "I(X;Y_t \\mid \\mathcal H_{t-1}) \\le C" in s
