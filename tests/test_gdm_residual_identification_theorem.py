#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ART = ROOT / "artifacts/chronos/gdm_residual_identification_theorem_2026_05_28.json"
DOC = ROOT / "docs/status/GDM_RESIDUAL_IDENTIFICATION_THEOREM_2026_05_28.md"
LEAN = ROOT / "lean/Chronos/Frontier/GDMResidualIdentificationTheorem.lean"
VERIFY = ROOT / "tools/verify_gdm_residual_identification_theorem.py"


def test_gdm_residual_identification_files_exist():
    assert ART.exists()
    assert DOC.exists()
    assert LEAN.exists()
    assert VERIFY.exists()


def test_gdm_residual_identification_verifier_passes():
    subprocess.run([sys.executable, str(VERIFY)], cwd=ROOT, check=True)
