from pathlib import Path

def test_newstein_twisted_fiber_rank_computation_locked():
    p = Path("docs/math/NEWSTEIN_TWISTED_FIBER_RANK_COMPUTATION.md")
    s = p.read_text()
    required = [
        "# Newstein Twisted Fiber Rank Computation",
        "## Target statement",
        "\\dim_{\\mathbb F_2}\\!\\bigl(Z_1(\\widetilde T^{\\mathrm{tw}})/W^{\\mathrm{tw}}\\bigr)=2.",
        "## Inputs",
        "### 1. Quotient-homology identification",
        "### 2. Connected twisted-cover structure",
        "## Required subclaims",
        "### 1. One-direction odd monodromy",
        "### 2. Connectedness of the twisted double cover",
        "### 3. Topological type of the connected cover",
        "### 4. Homology dimension of the connected lifted torus",
        "\\dim_{\\mathbb F_2} H_1(\\widetilde T^{\\mathrm{tw}};\\mathbb F_2)=2.",
        "## Deduction",
        "Hence",
        "## Status",
        "This is the second numerical rank computation in the Newstein fiber branch.",
        "## Dependencies discharged by this theorem",
        "1. The second half of the \\(4\\) versus \\(2\\) fiber-rank gap.",
        "2. Input to the fiber rank-gap theorem.",
        "3. Input to the global quotient-gap assembly.",
    ]
    for item in required:
        assert item in s
