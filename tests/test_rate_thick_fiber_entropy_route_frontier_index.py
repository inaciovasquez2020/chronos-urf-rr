import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_rate_thick_fiber_entropy_route_index_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_rate_thick_fiber_entropy_route_frontier_index.py"],
        cwd=ROOT,
        check=True,
    )

def test_rate_thick_fiber_entropy_route_index_status():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/rate_thick_fiber_entropy_route_frontier_index_2026_05_17.json").read_text()
    )
    assert artifact["status"] == "FRONTIER_OPEN"
    assert artifact["classification"] == "route_index_only"
    assert "DimensionRegularFiberGrowth" in artifact["route_inputs"]
    assert "RankRateToLyapunovExpansion" in artifact["route_inputs"]
    assert "FiberEntropyMassLowerBoundsUnstableEntropy" in artifact["route_inputs"]
    assert "RateThickPositiveEntropyLowerBound" in artifact["route_inputs"]

def test_rate_thick_fiber_entropy_route_index_no_overclaim():
    paths = [
        ROOT / "lean/Chronos/Frontier/RateThickFiberEntropyRouteFrontierIndex.lean",
        ROOT / "artifacts/chronos/rate_thick_fiber_entropy_route_frontier_index_2026_05_17.json",
        ROOT / "docs/status/RATE_THICK_FIBER_ENTROPY_ROUTE_FRONTIER_INDEX_2026_05_17.md",
    ]
    combined = "\n".join(path.read_text() for path in paths).lower()
    assert "proves ratethickfiberentropygap" not in combined
    assert "proves unrestricted universalfiberentropygap" not in combined
    assert "solves p vs np" not in combined
