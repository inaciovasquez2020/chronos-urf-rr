import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_unconditional_ufeg_obstruction_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_unconditional_universal_fiber_entropy_gap_obstruction.py"],
        cwd=ROOT,
        check=True,
    )

def test_unconditional_ufeg_obstruction_artifact_status() -> None:
    artifact = json.loads(
        (ROOT / "artifacts/chronos/unconditional_universal_fiber_entropy_gap_obstruction_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "UNCONDITIONAL_UFEG_OBSTRUCTED"

def test_unconditional_ufeg_obstruction_no_overclaim() -> None:
    combined = "\n".join(
        p.read_text()
        for p in [
            ROOT / "lean/Chronos/Frontier/UnconditionalUniversalFiberEntropyGapObstruction.lean",
            ROOT / "docs/status/UNCONDITIONAL_UNIVERSAL_FIBER_ENTROPY_GAP_OBSTRUCTION_2026_05_18.md",
        ]
    )
    forbidden = [
        "unrestricted Chronos-RR proved",
        "P vs NP proved",
        "Clay problem solved",
        "unconditional UniversalFiberEntropyGap proved",
    ]
    for token in forbidden:
        assert token not in combined
