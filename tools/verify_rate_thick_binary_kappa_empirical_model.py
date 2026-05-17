#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs/status/RATE_THICK_BINARY_KAPPA_EMPIRICAL_MODEL_2026_05_17.md"
ART = ROOT / "artifacts/chronos/rate_thick_binary_kappa_empirical_model_2026_05_17.json"
EXP = ROOT / "experiments/rate_thick_binary_kappa_empirical"

REQUIRED_FILES = [
    EXP / "urf_empirical_model.py",
    EXP / "holdout_compare.py",
    EXP / "loocv_ratio_stability.py",
    EXP / "ratio_stability_slack_compare.py",
    EXP / "sample_data.csv",
]

REQUIRED_DOC_PHRASES = [
    "EMPIRICAL_MODEL_ONLY / NO_THEOREM_PROMOTION",
    "Train-minimum kappa domination failed on holdout.",
    "Observed maximum slack required: `0.016941176470588237`.",
    "Empirical comparison only.",
    "Does not prove:",
    "entropy-minimum domination",
    "ratio stability",
    "uniform fiber-mass bound",
    "unrestricted RateThickFiberCoercivity",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

FORBIDDEN_DOC_PHRASES = [
    "proves entropy-minimum domination",
    "proves ratio stability",
    "proves uniform fiber-mass bound",
    "proves unrestricted RateThickFiberCoercivity",
    "proves unrestricted UniversalFiberEntropyGap",
    "proves Chronos-RR",
    "proves H4.1/FGL",
    "proves P vs NP",
    "proves any Clay problem",
    "theorem_promotion\": true",
]


def run(cmd: list[str]) -> str:
    proc = subprocess.run(
        cmd,
        cwd=EXP,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    return proc.stdout


def main() -> None:
    for path in REQUIRED_FILES:
        assert path.exists(), path

    doc = DOC.read_text()
    for phrase in REQUIRED_DOC_PHRASES:
        assert phrase in doc, phrase
    for phrase in FORBIDDEN_DOC_PHRASES:
        assert phrase not in doc, phrase

    data = json.loads(ART.read_text())
    assert data["status"] == "EMPIRICAL_MODEL_ONLY"
    assert data["theorem_promotion"] is False
    assert data["delta_observed_max"] == 0.016941176470588237
    assert data["train_min_domination_failures"] == 2
    assert data["loocv_train_min_domination_failures"] == 1
    assert data["holdout_safe_domination_failures"] == 0
    assert data["uniform_bound_failures"] == 0

    out1 = run([
        sys.executable,
        "urf_empirical_model.py",
        "--data",
        "sample_data.csv",
        "--outdir",
        "out_verify_model",
        "--alpha-quantile",
        "0.0",
        "--bootstrap",
        "25",
    ])
    assert '"binary_kappa_positive_failures": 0' in out1
    assert '"domination_failure_count": 0' in out1

    out2 = run([sys.executable, "holdout_compare.py"])
    assert '"train_min_domination_failures": 2' in out2
    assert '"holdout_safe_domination_failures": 0' in out2
    assert '"unrestricted_theorem_closure": "not_claimed"' in out2

    out3 = run([sys.executable, "loocv_ratio_stability.py"])
    assert '"train_min_domination_failures": 1' in out3
    assert '"max_slack_required": 0.016380952380952385' in out3
    assert '"unrestricted_theorem_closure": "not_claimed"' in out3

    out4 = run([sys.executable, "ratio_stability_slack_compare.py"])
    assert '"delta_observed_max": 0.016941176470588237' in out4
    assert '"holdout_slack"' in out4
    assert '"observed_max_slack"' in out4
    assert '"unrestricted_theorem_closure": "not_claimed"' in out4

    print("Rate-thick binary kappa empirical model verified.")


if __name__ == "__main__":
    main()
