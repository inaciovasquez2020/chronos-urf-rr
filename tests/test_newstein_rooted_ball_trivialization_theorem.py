from pathlib import Path

def test_newstein_rooted_ball_trivialization_theorem_locked():
    p = Path("docs/math/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION_THEOREM.md")
    s = p.read_text()
    required = [
        "# Newstein Rooted-Ball Trivialization Theorem",
        "## Target statement",
        "\\widetilde B_r^{\\mathrm{tw}}(x)\\cong \\widetilde B_r^{\\mathrm{triv}}(x).",
        "\\operatorname{Type}_{k,r}(G_n)=\\operatorname{Type}_{k,r}(H_n).",
        "## Inputs",
        "### 1. Local cycle-vanishing theorem",
        "### 2. Local coboundary theorem",
        "## Deduction",
        "Use \\(f_x\\) as the gauge change trivializing the twisted cocycle on \\(U\\).",
        "Therefore the twisted rooted ball and trivial rooted ball are isomorphic:",
        "Since rooted radius-\\(r\\) balls agree for every center,",
        "## Assembly theorem",
        "## Status",
        "This closes the rooted-ball branch of the Newstein chain at the theorem-ledger level.",
        "## Dependencies discharged by this theorem",
        "1. Local rooted-ball equivalence between twisted and trivial lifts.",
        "2. Equality of rooted radius-\\(r\\) type data.",
        "3. The local side of the non-factorization setup.",
    ]
    for item in required:
        assert item in s
