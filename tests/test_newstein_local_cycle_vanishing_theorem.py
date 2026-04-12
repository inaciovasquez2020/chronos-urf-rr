from pathlib import Path

def test_newstein_local_cycle_vanishing_theorem_locked():
    p = Path("docs/math/NEWSTEIN_LOCAL_CYCLE_VANISHING_THEOREM.md")
    s = p.read_text()
    required = [
        "# Newstein Local Cycle-Vanishing Theorem",
        "## Target statement",
        "For every \\(x \\in V(B_n)\\) and every local cycle \\(C \\subseteq B_r^{B_n}(x)\\),",
        "\\phi_H(C)=0.",
        "## Inputs",
        "### 1. Local triangle-generation theorem",
        "### 2. Triangle-vanishing theorem",
        "## Deduction",
        "By local triangle-generation,",
        "By additivity of \\(\\phi_H\\),",
        "By triangle-vanishing,",
        "Hence",
        "## Assembly theorem",
        "## Status",
        "This is the derived closure step between triangle-vanishing and local coboundary.",
        "## Dependencies discharged by this theorem",
        "1. Input to the local coboundary theorem.",
        "2. Input to rooted-ball trivialization.",
        "3. Input to local-type equality in the Newstein chain.",
    ]
    for item in required:
        assert item in s
