from pathlib import Path

def test_newstein_transcript_lower_bound_locked():
    p = Path("docs/math/NEWSTEIN_TRANSCRIPT_LOWER_BOUND.md")
    s = p.read_text()
    required = [
        "# Newstein Transcript Lower Bound",
        "## Target statement",
        "T_n \\ge \\frac{2|V(X_n)|}{C}.",
        "T_n=\\Omega(n).",
        "## Inputs",
        "### 1. Global quotient-gap theorem",
        "### 2. Per-step information bound",
        "## Required subclaims",
        "### 1. Total transcript budget after \\(T_n\\) steps",
        "### 2. Obstruction resolution demand",
        "### 3. Comparison inequality",
        "## Deduction",
        "Therefore",
        "## Assembly theorem",
        "## Status",
        "This is the final theorem-level target in the Newstein complexity branch.",
        "## Dependencies discharged by this theorem",
        "1. Completion of the Newstein lower-bound branch.",
        "2. Final linear transcript obstruction statement.",
        "3. End-to-end reduction closure at the theorem-ledger level.",
    ]
    for item in required:
        assert item in s
