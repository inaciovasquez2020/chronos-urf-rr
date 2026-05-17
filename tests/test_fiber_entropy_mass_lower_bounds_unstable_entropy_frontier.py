import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_fiber_entropy_mass_lower_bounds_unstable_entropy_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_fiber_entropy_mass_lower_bounds_unstable_entropy_frontier.py"],
        cwd=ROOT,
        check=True,
    )

def test_fiber_entropy_mass_lower_bounds_unstable_entropy_status_is_frontier_open():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/fiber_entropy_mass_lower_bounds_unstable_entropy_frontier_2026_05_17.json").read_text()
    )
    assert artifact["status"] == "FRONTIER_OPEN"
    assert artifact["classification"] == "theorem_target_only"
    assert "FiberEntropyMassLowerBoundsUnstableEntropy" in artifact["missing_theorem_target"]

def test_fiber_entropy_mass_lower_bounds_unstable_entropy_no_overclaim():
    paths = [
        ROOT / "lean/Chronos/Frontier/FiberEntropyMassLowerBoundsUnstableEntropyFrontier.lean",
        ROOT / "artifacts/chronos/fiber_entropy_mass_lower_bounds_unstable_entropy_frontier_2026_05_17.json",
        ROOT / "docs/status/FIBER_ENTROPY_MASS_LOWER_BOUNDS_UNSTABLE_ENTROPY_FRONTIER_2026_05_17.md",
    ]
    combined = "\n".join(path.read_text() for path in paths).lower()
    assert "proves fiberentropymasslowerboundsunstableentropy" not in combined
    assert "proves unrestricted universalfiberentropygap" not in combined
    assert "solves p vs np" not in combined
