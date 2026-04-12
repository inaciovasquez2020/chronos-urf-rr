from pathlib import Path

def test_newstein_local_triangle_generation_theorem_locked():
    p = Path("docs/math/NEWSTEIN_LOCAL_TRIANGLE_GENERATION_THEOREM.md")
    s = p.read_text()
    required = [
        "# Newstein Local Triangle-Generation Theorem",
        "## Target statement",
        "For every \\(x \\in V(B_n)\\),",
        "### 1. No torus-fiber wrap in radius-\\(r\\) balls",
        "L > 2r+1",
        "### 2. No backbone cycle in radius-\\(r\\) balls",
        "\\operatorname{girth}(X_n) > 2r+1",
        "### 3. Local simple connectivity",
        "### 4. Triangle-boundary generation",
        "## Assembly theorem",
        "## Status",
        "This is the next theorem-level closure target in the Newstein rooted-ball branch.",
        "## Dependencies discharged by this theorem",
        "1. Local cycle generation inside rooted radius-\\(r\\) balls.",
        "2. Input to triangle-vanishing \\(\\Rightarrow\\) local cycle-vanishing.",
        "3. Input to rooted-ball trivialization.",
        "4. Input to the local-type equality branch of the Newstein chain.",
    ]
    for item in required:
        assert item in s
