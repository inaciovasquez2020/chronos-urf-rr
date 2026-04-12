from pathlib import Path

def test_newstein_direct_sum_independence_assembly_locked():
    p = Path("docs/math/NEWSTEIN_DIRECT_SUM_INDEPENDENCE_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Direct-Sum Independence Assembly" in s
    assert "## Status\nOPEN" in s
    assert "\\operatorname{rank}\\!\\left(\\sum_i Q_i\\right)=\\sum_i \\operatorname{rank}(Q_i)" in s
    assert "## Assembly inputs" in s
    assert "Fiber quotient-rank assembly." in s
    assert "Rank additivity on direct sums." in s
    assert "## Proof skeleton" in s
    assert "\\bigoplus_i Q_i" in s
    assert "\\mathrm{DirectSumIndependence}" in s
    assert "\\mathrm{FiberToGlobalInjection}" in s
