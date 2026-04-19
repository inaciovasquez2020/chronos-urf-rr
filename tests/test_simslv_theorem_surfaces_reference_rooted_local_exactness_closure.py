from pathlib import Path

TARGETS = [
    "docs/math/SIMSLV_LOCAL_TRIANGLE_PREDICATE_THEOREM.md",
    "docs/math/SIMSLV_BALL_SIMPLE_CONNECTEDNESS_THEOREM.md",
    "docs/math/SIMSLV_TRIANGLE_VANISHING_THEOREM.md",
    "docs/math/SIMSLV_LOCAL_COBOUNDARY_TRIVIALIZATION_THEOREM.md",
]

def test_simslv_theorem_surfaces_reference_rooted_local_exactness_closure() -> None:
    for path in TARGETS:
        s = Path(path).read_text()
        assert "docs/math/SIMSLV_ROOTED_LOCAL_EXACTNESS_CLOSURE.md" in s
