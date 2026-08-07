from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/gfe/certify_gfe_soi_leading_fredholm_obstruction.py"
ARTIFACT = ROOT / "artifacts/chronos/gfe_soi_leading_fredholm_obstruction.json"


def test_gfe_soi_leading_fredholm_obstruction(tmp_path: Path) -> None:
    generated = tmp_path / "certificate.json"

    subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--output",
            str(generated),
        ],
        cwd=ROOT,
        check=True,
    )

    committed = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    fresh = json.loads(generated.read_text(encoding="utf-8"))

    assert fresh == committed

    assert committed["normalization"]["A_EH"] == "1/2"
    assert (
        committed["normalization"]
        ["principal_balanced_characteristic_at_x4"]
        == "(mu^2 + 12/5)^2"
    )
    assert committed["leading_fredholm_order"] == "q^3"

    lower = Fraction(
        committed["certified_real_part"]["lower_exact"]
    )
    upper = Fraction(
        committed["certified_real_part"]["upper_exact"]
    )

    assert lower > Fraction(1, 605)
    assert upper < Fraction(1, 600)
    assert lower > 0

    assert (
        committed["result"]
        == "leading q^3 Fredholm coefficient is uniformly nonzero "
           "on the certified q->0 crossing/frequency box"
    )

    assert (
        committed["boundary"]
        ["finite_q_interval_newton_through_q_1e_minus_2"]
        == "not claimed"
    )
    assert (
        committed["boundary"]
        ["nonexistence_of_all_deformed_invariant_graphs"]
        == "not claimed"
    )
    assert (
        committed["boundary"]
        ["full_theory_220_qnm_tail_transfer"]
        == "prohibited"
    )
