from pathlib import Path

def test_newstein_remaining_theorem_level_obligations_locked():
    p = Path("docs/math/NEWSTEIN_REMAINING_THEOREM_LEVEL_OBLIGATIONS.md")
    s = p.read_text()
    required = [
        "# Remaining theorem-level obligations in the Newstein chain",
        "## I. Rooted-ball branch",
        "### I.1 Local triangle-generation theorem",
        "### I.2 Triangle-vanishing theorem",
        "### I.5 Rooted-ball trivialization theorem",
        "## II. Fiber quotient-rank branch",
        "### II.2 Trivial fiber rank computation",
        "### II.3 Twisted fiber rank computation",
        "## III. Fiber-to-global branch",
        "### III.1 Injectivity for one fiber",
        "### III.3 Direct-sum embedding",
        "## IV. Global assembly branch",
        "### IV.1 Quotient-gap theorem",
        "## V. Complexity/lower-bound branch",
        "### V.1 Per-step information bound",
        "## Minimal closure set",
        "1. Local triangle-generation theorem.",
        "2. Triangle-vanishing theorem.",
        "3. Fiber quotient-rank computation \\(4\\) vs. \\(2\\).",
        "4. Fiber-to-global injectivity/direct-sum independence.",
        "5. Per-step information bound.",
        "`chronos-urf-rr`: reduction-complete, theorem-incomplete.",
    ]
    for item in required:
        assert item in s
