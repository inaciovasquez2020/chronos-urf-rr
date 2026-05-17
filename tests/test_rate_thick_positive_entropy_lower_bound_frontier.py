import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_rate_thick_positive_entropy_lower_bound_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_rate_thick_positive_entropy_lower_bound_frontier.py"],
        cwd=ROOT,
        check=True,
    )

def test_rate_thick_positive_entropy_lower_bound_status_is_frontier_open():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/rate_thick_positive_entropy_lower_bound_frontier_2026_05_17.json").read_text()
    )
    assert artifact["status"] == "FRONTIER_OPEN"
    assert artifact["classification"] == "theorem_target_only"
    assert "for every lam > 0, there exists eps > 0 such that RateThickPositiveEntropyLowerBound lam eps" in artifact["missing_theorem_target"]

def test_rate_thick_positive_entropy_lower_bound_no_overclaim():
    paths = [
        ROOT / "lean/Chronos/Frontier/RateThickPositiveEntropyLowerBoundFrontier.lean",
        ROOT / "artifacts/chronos/rate_thick_positive_entropy_lower_bound_frontier_2026_05_17.json",
        ROOT / "docs/status/RATE_THICK_POSITIVE_ENTROPY_LOWER_BOUND_FRONTIER_2026_05_17.md",
    ]
    combined = "\n".join(path.read_text() for path in paths).lower()
    assert "proves ratethickpositiveentropylowerbound" not in combined
    assert "proves unrestricted universalfiberentropygap" not in combined
    assert "solves p vs np" not in combined
