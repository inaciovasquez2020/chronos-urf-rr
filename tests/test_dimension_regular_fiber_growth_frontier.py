import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_dimension_regular_fiber_growth_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_dimension_regular_fiber_growth_frontier.py"],
        cwd=ROOT,
        check=True,
    )

def test_dimension_regular_fiber_growth_status_is_frontier_open():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/dimension_regular_fiber_growth_frontier_2026_05_17.json").read_text()
    )
    assert artifact["status"] == "FRONTIER_OPEN"
    assert artifact["classification"] == "theorem_target_only"
    assert "for every lam > 0, DimensionRegularFiberGrowth lam" in artifact["missing_theorem_target"]

def test_dimension_regular_fiber_growth_no_overclaim():
    paths = [
        ROOT / "lean/Chronos/Frontier/DimensionRegularFiberGrowthFrontier.lean",
        ROOT / "artifacts/chronos/dimension_regular_fiber_growth_frontier_2026_05_17.json",
        ROOT / "docs/status/DIMENSION_REGULAR_FIBER_GROWTH_FRONTIER_2026_05_17.md",
    ]
    combined = "\n".join(path.read_text() for path in paths).lower()
    assert "proves dimensionsregularfibergrowth" not in combined
    assert "proves unrestricted universalfiberentropygap" not in combined
    assert "solves p vs np" not in combined
