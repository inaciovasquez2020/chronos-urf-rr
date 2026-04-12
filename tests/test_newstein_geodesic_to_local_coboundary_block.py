from pathlib import Path

def test_newstein_geodesic_to_local_coboundary_block_lock():
    s = Path("docs/math/NEWSTEIN_GEODESIC_TO_LOCAL_COBOUNDARY_BLOCK.md").read_text()
    assert "# Newstein Geodesic-to-Local-Coboundary Block" in s
    assert "## Status\nOPEN" in s
    assert "NEWSTEIN_LOCAL_COBOUNDARY_CRITERION.md" in s
