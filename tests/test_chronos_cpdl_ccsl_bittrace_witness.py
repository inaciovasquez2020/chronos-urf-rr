from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_cpdl_ccsl_bittrace_artifact(): assert json.loads((ROOT / "artifacts/chronos/cpdl_ccsl_bittrace_witness.json").read_text())["status"] == "MODEL_WITNESS_ONLY"

def test_cpdl_ccsl_bittrace_boundary(): assert "does not prove P vs NP closure" in (ROOT / "docs/status/CHRONOS_CPDL_CCSL_BITTRACE_WITNESS_2026_05_05.md").read_text()

def test_cpdl_ccsl_bittrace_verifier_passes(): assert "MODEL_WITNESS_ONLY" in subprocess.run(["python3", "tools/verify_chronos_cpdl_ccsl_bittrace_witness.py"], cwd=ROOT, check=True, capture_output=True, text=True).stdout
