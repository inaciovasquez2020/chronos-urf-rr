import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_rank_rate_to_lyapunov_expansion_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_rank_rate_to_lyapunov_expansion_frontier.py"],
        cwd=ROOT,
        check=True,
    )

def test_rank_rate_to_lyapunov_expansion_status_is_frontier_open():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/rank_rate_to_lyapunov_expansion_frontier_2026_05_17.json").read_text()
    )
    assert artifact["status"] == "FRONTIER_OPEN"
    assert artifact["classification"] == "theorem_target_only"
    assert "for every lam > 0, RankRateToLyapunovExpansion lam" in artifact["missing_theorem_target"]

def test_rank_rate_to_lyapunov_expansion_no_overclaim():
    paths = [
        ROOT / "lean/Chronos/Frontier/RankRateToLyapunovExpansionFrontier.lean",
        ROOT / "artifacts/chronos/rank_rate_to_lyapunov_expansion_frontier_2026_05_17.json",
        ROOT / "docs/status/RANK_RATE_TO_LYAPUNOV_EXPANSION_FRONTIER_2026_05_17.md",
    ]
    combined = "\n".join(path.read_text() for path in paths).lower()
    assert "proves rankratetolyapunovexpansion" not in combined
    assert "proves unrestricted universalfiberentropygap" not in combined
    assert "solves p vs np" not in combined
