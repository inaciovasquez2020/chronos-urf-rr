from pathlib import Path

def test_newstein_non_factorization_consequence_locked():
    p = Path("docs/math/NEWSTEIN_NON_FACTORIZATION_CONSEQUENCE.md")
    s = p.read_text()
    required = [
        "# Newstein Non-Factorization Consequence",
        "## Target statement",
        "Q(G_n)\\neq Q(H_n)",
        "does not factor through rooted radius-\\(r\\) type or \\(FO^k_r\\)-type",
        "## Inputs",
        "### 1. Rooted-ball trivialization",
        "### 2. Global quotient-gap theorem",
        "## Required subclaims",
        "### 1. Factorization implication",
        "### 2. \\(FO^k_r\\)-type implication",
        "### 3. Contradiction step",
        "## Deduction",
        "Contradiction.",
        "Therefore \\(Q\\) does not factor through rooted radius-\\(r\\) type or \\(FO^k_r\\)-type.",
        "## Assembly theorem",
        "## Status",
        "This closes the non-factorization branch of the Newstein chain at the theorem-ledger level.",
        "## Dependencies discharged by this theorem",
        "1. Final structural obstruction statement for the Newstein quotient invariant.",
        "2. Input to the complexity/lower-bound branch.",
        "3. Local-versus-global separation certificate in the Newstein chain.",
    ]
    for item in required:
        assert item in s
