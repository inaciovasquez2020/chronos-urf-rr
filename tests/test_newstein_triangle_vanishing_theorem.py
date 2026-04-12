from pathlib import Path

def test_newstein_triangle_vanishing_theorem_locked():
    p = Path("docs/math/NEWSTEIN_TRIANGLE_VANISHING_THEOREM.md")
    s = p.read_text()
    required = [
        "# Newstein Triangle-Vanishing Theorem",
        "## Target statement",
        "For every local triangle \\(\\tau\\),",
        "\\phi_H(\\partial \\tau)=0.",
        "## Required subclaims",
        "### 1. Explicit cocycle definition",
        "### 2. Triangle-type classification",
        "### 3. Parity verification on each triangle type",
        "### 4. Additivity on boundary sums",
        "## Assembly theorem",
        "## Status",
        "This is the next theorem-level closure target after local triangle-generation.",
        "## Dependencies discharged by this theorem",
        "1. Input to local cycle-vanishing.",
        "2. Input to rooted-ball trivialization.",
        "3. Input to local-type equality in the Newstein chain.",
    ]
    for item in required:
        assert item in s
