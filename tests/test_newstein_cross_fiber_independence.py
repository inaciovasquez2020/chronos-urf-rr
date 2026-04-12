from pathlib import Path

def test_newstein_cross_fiber_independence_locked():
    p = Path("docs/math/NEWSTEIN_CROSS_FIBER_INDEPENDENCE.md")
    s = p.read_text()
    required = [
        "# Newstein Cross-Fiber Independence",
        "## Target statement",
        "\\operatorname{im}(\\iota_u)\\cap \\operatorname{im}(\\iota_v)=0",
        "## Inputs",
        "### 1. Fiber-to-global injectivity",
        "### 2. Fiber decomposition",
        "## Required subclaims",
        "### 1. Disjoint fiber support at the quotient-generator level",
        "### 2. Connector edges do not identify fiber classes",
        "### 3. Mixed local-ball relations do not collapse distinct fiber classes",
        "### 4. Zero-intersection criterion",
        "## Deduction",
        "Therefore",
        "## Assembly theorem",
        "## Status",
        "This is the second theorem-level target in the fiber-to-global branch.",
        "## Dependencies discharged by this theorem",
        "1. Input to the direct-sum embedding theorem.",
        "2. Input to the global quotient-gap theorem.",
        "3. Separation of per-fiber contributions in the Newstein assembly.",
    ]
    for item in required:
        assert item in s
