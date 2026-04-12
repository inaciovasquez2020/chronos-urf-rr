from pathlib import Path

def test_newstein_fiber_rank_gap_theorem_locked():
    p = Path("docs/math/NEWSTEIN_FIBER_RANK_GAP_THEOREM.md")
    s = p.read_text()
    required = [
        "# Newstein Fiber Rank-Gap Theorem",
        "## Target statement",
        "\\dim_{\\mathbb F_2}\\!\\bigl(Z_1(\\widetilde T_v^{\\mathrm{triv}})/W_v^{\\mathrm{triv}}\\bigr)",
        "\\dim_{\\mathbb F_2}\\!\\bigl(Z_1(\\widetilde T_v^{\\mathrm{tw}})/W_v^{\\mathrm{tw}}\\bigr)",
        "=2.",
        "## Inputs",
        "### 1. Trivial fiber rank computation",
        "### 2. Twisted fiber rank computation",
        "## Deduction",
        "4-2=2.",
        "## Assembly theorem",
        "## Status",
        "This closes the numerical fiber-rank branch of the Newstein chain at the theorem-ledger level.",
        "## Dependencies discharged by this theorem",
        "1. Per-fiber quantitative input to the global quotient-gap theorem.",
        "2. Numerical bridge from fiber topology to global obstruction growth.",
        "3. The fiber-side contribution needed for \\(\\Omega(n)\\) assembly.",
    ]
    for item in required:
        assert item in s
