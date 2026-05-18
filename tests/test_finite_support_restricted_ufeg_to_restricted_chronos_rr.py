import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_finite_support_restricted_ufeg_to_restricted_chronos_rr_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_finite_support_restricted_ufeg_to_restricted_chronos_rr.py"],
        cwd=ROOT,
        check=True,
    )

def test_finite_support_restricted_ufeg_to_restricted_chronos_rr_artifact_status() -> None:
    artifact = json.loads(
        (ROOT / "artifacts/chronos/finite_support_restricted_ufeg_to_restricted_chronos_rr_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "FINITE_SUPPORT_RESTRICTED_UFEG_TO_RESTRICTED_CHRONOS_RR_CLOSED"

def test_finite_support_restricted_ufeg_to_restricted_chronos_rr_no_overclaim() -> None:
    combined = "\n".join(
        p.read_text()
        for p in [
            ROOT / "lean/Chronos/Frontier/FiniteSupportRestrictedUFEGToRestrictedChronosRR.lean",
            ROOT / "docs/status/FINITE_SUPPORT_RESTRICTED_UFEG_TO_RESTRICTED_CHRONOS_RR_2026_05_18.md",
        ]
    )
    forbidden = [
        "unrestricted UniversalFiberEntropyGap proved",
        "unrestricted Chronos-RR proved",
        "unrestricted H4.1/FGL proved",
        "P vs NP proved",
        "Clay problem solved",
    ]
    for token in forbidden:
        assert token not in combined
