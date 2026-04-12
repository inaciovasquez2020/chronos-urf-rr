from pathlib import Path

def test_newstein_fiber_to_global_injection_assembly_locked():
    p = Path("docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTION_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Fiber-to-Global Injection Assembly" in s
    assert "## Status\nOPEN" in s
    assert "\\iota:\\bigoplus_i Q_i \\hookrightarrow Q_{\\mathrm{global}}" in s
    assert "## Assembly inputs" in s
    assert "Direct-sum independence assembly." in s
    assert "Trivial-kernel criterion for injectivity." in s
    assert "## Proof skeleton" in s
    assert "\\ker(\\iota)=0" in s
    assert "\\mathrm{FiberToGlobalInjection}" in s
    assert "\\mathrm{PerStepInformationBound}" in s
