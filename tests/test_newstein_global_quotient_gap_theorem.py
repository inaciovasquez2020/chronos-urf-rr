from pathlib import Path

def test_newstein_global_quotient_gap_theorem_locked():
    p = Path("docs/math/NEWSTEIN_GLOBAL_QUOTIENT_GAP_THEOREM.md")
    s = p.read_text()
    required = [
        "# Newstein Global Quotient-Gap Theorem",
        "## Target statement",
        "\\dim_{\\mathbb F_2}Q(G_n)-\\dim_{\\mathbb F_2}Q(H_n)\\ge 2|V(X_n)|.",
        "\\dim_{\\mathbb F_2}Q(G_n)-\\dim_{\\mathbb F_2}Q(H_n)=\\Omega(n).",
        "## Inputs",
        "### 1. Rooted-ball trivialization",
        "### 2. Fiber rank-gap theorem",
        "### 3. Direct-sum embedding",
        "## Required subclaims",
        "### 1. Trivial global lower bound",
        "### 2. Twisted global lower bound",
        "### 3. Fiberwise accumulation",
        "### 4. Global gap transfer",
        "## Deduction",
        "## Assembly theorem",
        "## Status",
        "This is the first global assembly target in the Newstein chain.",
        "## Dependencies discharged by this theorem",
        "1. Input to non-factorization.",
        "2. Input to transcript lower bounds.",
        "3. Global linear-growth obstruction in the Newstein chain.",
    ]
    for item in required:
        assert item in s
