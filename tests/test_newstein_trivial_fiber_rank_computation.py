from pathlib import Path

def test_newstein_trivial_fiber_rank_computation_locked():
    p = Path("docs/math/NEWSTEIN_TRIVIAL_FIBER_RANK_COMPUTATION.md")
    s = p.read_text()
    required = [
        "# Newstein Trivial Fiber Rank Computation",
        "## Target statement",
        "\\dim_{\\mathbb F_2}\\!\\bigl(Z_1(\\widetilde T^{\\mathrm{triv}})/W^{\\mathrm{triv}}\\bigr)=4.",
        "## Inputs",
        "### 1. Quotient-homology identification",
        "### 2. Trivial-cover decomposition",
        "\\widetilde T^{\\mathrm{triv}} \\cong T \\sqcup T.",
        "## Required subclaims",
        "### 1. Homology of one torus",
        "\\dim_{\\mathbb F_2} H_1(T;\\mathbb F_2)=2.",
        "### 2. Homology of a disjoint union",
        "### 3. Dimension count",
        "## Deduction",
        "Hence",
        "## Status",
        "This is the first numerical rank computation in the Newstein fiber branch.",
        "## Dependencies discharged by this theorem",
        "1. One half of the \\(4\\) versus \\(2\\) fiber-rank gap.",
        "2. Input to the fiber rank-gap theorem.",
        "3. Input to the global quotient-gap assembly.",
    ]
    for item in required:
        assert item in s
