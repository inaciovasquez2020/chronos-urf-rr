from pathlib import Path

def test_newstein_fiber_to_global_injectivity_locked():
    p = Path("docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTIVITY.md")
    s = p.read_text()
    required = [
        "# Newstein Fiber-to-Global Injectivity",
        "## Target statement",
        "\\iota_v^{\\mathrm{triv}}",
        "\\iota_v^{\\mathrm{tw}}",
        "## Required subclaims",
        "### 1. Fiber support survives local-ball quotienting",
        "### 2. Local-ball relations remain locally generated",
        "### 3. Fiber quotient classes are globally nonlocal",
        "### 4. Inclusion descends to quotient",
        "## Deduction",
        "Hence the induced map is injective.",
        "## Assembly theorem",
        "## Status",
        "This is the first theorem-level target in the fiber-to-global branch.",
        "## Dependencies discharged by this theorem",
        "1. Input to cross-fiber independence.",
        "2. Input to the direct-sum embedding theorem.",
        "3. Input to global quotient-gap assembly.",
    ]
    for item in required:
        assert item in s
