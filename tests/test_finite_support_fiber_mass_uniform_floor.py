import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_finite_support_fiber_mass_uniform_floor_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_finite_support_fiber_mass_uniform_floor.py"],
        cwd=ROOT,
        check=True,
    )

def test_finite_support_fiber_mass_uniform_floor_artifact_status() -> None:
    artifact = json.loads(
        (ROOT / "artifacts/chronos/finite_support_fiber_mass_uniform_floor_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "FINITE_SUPPORT_FIBER_MASS_UNIFORM_FLOOR_CLOSED"

def test_finite_support_fiber_mass_uniform_floor_no_overclaim() -> None:
    combined = "\n".join(
        p.read_text()
        for p in [
            ROOT / "lean/Chronos/Frontier/FiniteSupportFiberMassUniformFloor.lean",
            ROOT / "docs/status/FINITE_SUPPORT_FIBER_MASS_UNIFORM_FLOOR_2026_05_18.md",
        ]
    )
    forbidden = [
        "unrestricted UniversalFiberEntropyGap proved",
        "unrestricted Chronos-RR proved",
        "P vs NP proved",
        "Clay problem solved",
    ]
    for token in forbidden:
        assert token not in combined
