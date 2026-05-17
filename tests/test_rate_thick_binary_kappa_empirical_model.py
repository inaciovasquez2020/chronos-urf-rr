from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_empirical_model_status_doc_boundary():
    doc = (ROOT / "docs/status/RATE_THICK_BINARY_KAPPA_EMPIRICAL_MODEL_2026_05_17.md").read_text()
    assert "EMPIRICAL_MODEL_ONLY / NO_THEOREM_PROMOTION" in doc
    assert "Train-minimum kappa domination failed on holdout." in doc
    assert "Observed maximum slack required: `0.016941176470588237`." in doc
    assert "Empirical comparison only." in doc
    assert "Does not prove:" in doc
    assert "entropy-minimum domination" in doc
    assert "ratio stability" in doc
    assert "uniform fiber-mass bound" in doc
    assert "unrestricted UniversalFiberEntropyGap" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc


def test_empirical_model_artifact_boundary():
    data = json.loads(
        (ROOT / "artifacts/chronos/rate_thick_binary_kappa_empirical_model_2026_05_17.json").read_text()
    )
    assert data["status"] == "EMPIRICAL_MODEL_ONLY"
    assert data["theorem_promotion"] is False
    assert data["delta_observed_max"] == 0.016941176470588237
    assert data["train_min_domination_failures"] == 2
    assert data["loocv_train_min_domination_failures"] == 1
    assert data["holdout_safe_domination_failures"] == 0


def test_empirical_model_verifier_passes():
    subprocess.run(
        [sys.executable, "tools/verify_rate_thick_binary_kappa_empirical_model.py"],
        cwd=ROOT,
        check=True,
    )
