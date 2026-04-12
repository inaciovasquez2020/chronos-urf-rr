from pathlib import Path

def test_newstein_local_coboundary_theorem_locked():
    p = Path("docs/math/NEWSTEIN_LOCAL_COBOUNDARY_THEOREM.md")
    s = p.read_text()
    required = [
        "# Newstein Local Coboundary Theorem",
        "## Target statement",
        "Let \\(U\\) be a connected local subgraph.",
        "\\phi(C)=0",
        "there exists",
        "\\phi=\\delta f",
        "## Required subclaims",
        "### 1. Path-difference produces a cycle",
        "### 2. Path integral is endpoint-defined",
        "### 3. Edgewise coboundary identity",
        "## Deduction",
        "Hence path integrals agree, so \\(f\\) is well-defined.",
        "Therefore",
        "## Assembly theorem",
        "## Status",
        "This is the next theorem-level closure target after local cycle-vanishing.",
        "## Dependencies discharged by this theorem",
        "1. Input to rooted-ball trivialization.",
        "2. Input to local-type equality in the Newstein chain.",
        "3. Completion of the rooted-ball cocycle-trivialization branch.",
    ]
    for item in required:
        assert item in s
