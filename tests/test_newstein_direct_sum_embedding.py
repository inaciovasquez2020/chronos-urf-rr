from pathlib import Path

def test_newstein_direct_sum_embedding_locked():
    p = Path("docs/math/NEWSTEIN_DIRECT_SUM_EMBEDDING.md")
    s = p.read_text()
    required = [
        "# Newstein Direct-Sum Embedding",
        "## Target statement",
        "\\bigoplus_v Z_1(\\widetilde T_v^{\\mathrm{triv}})/W_v^{\\mathrm{triv}}",
        "\\bigoplus_v Z_1(\\widetilde T_v^{\\mathrm{tw}})/W_v^{\\mathrm{tw}}",
        "## Inputs",
        "### 1. Fiber-to-global injectivity",
        "### 2. Cross-fiber independence",
        "## Required subclaims",
        "### 1. Finite external direct sum map",
        "### 2. Well-definedness",
        "### 3. Kernel triviality",
        "## Deduction",
        "Therefore \\(\\Iota\\) is injective.",
        "## Assembly theorem",
        "## Status",
        "This closes the fiber-to-global branch of the Newstein chain at the theorem-ledger level.",
        "## Dependencies discharged by this theorem",
        "1. Input to the global quotient-gap theorem.",
        "2. Global accumulation mechanism for the per-fiber rank gap.",
        "3. Linear-growth assembly step in the Newstein chain.",
    ]
    for item in required:
        assert item in s
