import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_carrier_rank_soundness_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_carrier_rank_soundness.py"],
        cwd=ROOT,
        check=True,
    )


def test_carrier_rank_soundness_has_no_sorry_admit_axiom() -> None:
    lean = (ROOT / "lean/Chronos/Frontier/CarrierRankSoundness.lean").read_text()
    assert "sorry" not in lean
    assert "admit" not in lean
    assert "axiom " not in lean
