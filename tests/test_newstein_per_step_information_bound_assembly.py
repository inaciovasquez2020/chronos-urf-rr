from pathlib import Path

def test_newstein_per_step_information_bound_assembly_locked():
    p = Path("docs/math/NEWSTEIN_PER_STEP_INFORMATION_BOUND_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Per-Step Information Bound Assembly" in s
    assert "## Status\nOPEN" in s
    assert "\\iota:\\bigoplus_i Q_i \\hookrightarrow Q_{\\mathrm{global}}" in s
    assert "\\Delta_t \\leq \\operatorname{rank}(Q_{\\mathrm{global}}^{(t)})-\\operatorname{rank}(Q_{\\mathrm{global}}^{(t-1)})" in s
    assert "## Assembly inputs" in s
    assert "Fiber-to-global injection assembly." in s
    assert "Rank monotonicity under admissible quotient refinement." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{PerStepInformationBound}" in s
    assert "\\mathrm{AssemblyTheorem}" in s
