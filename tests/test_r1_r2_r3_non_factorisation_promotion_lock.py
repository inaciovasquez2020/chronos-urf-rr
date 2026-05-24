import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_r1_r2_r3_non_factorisation_promotion_lock_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_r1_r2_r3_non_factorisation_promotion_lock.py"],
        cwd=ROOT,
        check=True,
    )

def test_r1_r2_r3_non_factorisation_promotion_lock_artifact_status() -> None:
    artifact = json.loads(
        (
            ROOT
            / "artifacts/chronos/r1_r2_r3_non_factorisation_promotion_lock_2026_05_24.json"
        ).read_text()
    )
    assert artifact["status"] == "CONDITIONAL_INTERFACE_AND_NO_PROMOTION_LOCK_ONLY"
    assert artifact["conditional_chain"] == "R1_R2_R3_TO_NON_FACTORISATION"

def test_r1_r2_r3_non_factorisation_promotion_lock_no_overclaim() -> None:
    combined = "\n".join(
        p.read_text()
        for p in [
            ROOT / "lean/Chronos/Frontier/R1R2R3NonFactorisationPromotionLock.lean",
            ROOT / "docs/status/R1_R2_R3_NON_FACTORISATION_PROMOTION_LOCK_2026_05_24.md",
            ROOT / "artifacts/chronos/r1_r2_r3_non_factorisation_promotion_lock_2026_05_24.json",
        ]
    )
    forbidden = [
        "proved NON_FACTORISATION",
        "proved Chronos-RR",
        "proved H4.1/FGL",
        "P vs NP proved",
        "Clay problem solved",
    ]
    for token in forbidden:
        assert token not in combined
