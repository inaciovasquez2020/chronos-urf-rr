from pathlib import Path

def test_newstein_per_step_information_bound_locked():
    p = Path("docs/math/NEWSTEIN_PER_STEP_INFORMATION_BOUND.md")
    s = p.read_text()
    required = [
        "# Newstein Per-Step Information Bound",
        "## Target statement",
        "\\Delta I_t \\le C",
        "## Required model ingredients",
        "### 1. Admissible refinement state",
        "### 2. Transcript observable",
        "### 3. Locality / bounded-width constraint",
        "### 4. Uniform encoding bound",
        "## Required subclaims",
        "### 1. Conditional information increment formula",
        "### 2. Bounded choice family",
        "### 3. Entropy ceiling",
        "## Deduction",
        "Therefore",
        "## Status",
        "This is the critical remaining theorem-level target in the Newstein complexity branch.",
        "## Dependencies discharged by this theorem",
        "1. Input to the transcript lower bound.",
        "2. Completion of the linear-time obstruction branch.",
        "3. Final bridge from quotient-gap separation to refinement complexity.",
    ]
    for item in required:
        assert item in s
