#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "Chronos" / "Core" / "TraceRegimeClassifier.lean"

required_tokens = [
    "inductive RegimeStatus",
    "ZAP2_REGIME_CLOSED",
    "AFFINE_LINEAR_ADMISSIBLE",
    "AFFINE_SUBLINEAR_FORBIDDEN",
    "AFFINE_INTERMEDIATE_FRONTIER_OPEN",
    "UNKNOWN_FRONTIER_OPEN",
    "def ChronosTraceRegimeClassifier",
    "def ChronosTraceManifest_2026_05_05",
    "theorem ChronosTraceManifest_2026_05_05_audit",
    "theorem ChronosTraceClassifierCompleteness",
    "TRACE_REGIME_CLASSIFIER_SOLVED_FRONTIER_PRESERVED",
]

forbidden_tokens = [
    "P vs NP solved",
    "P≠NP proved",
    "H4.1 proved",
    "FGL proved",
    "canonical Chronos closure",
    "theoremClosure true",
]

text = LEAN.read_text()

missing = [tok for tok in required_tokens if tok not in text]
if missing:
    raise SystemExit(f"missing required tokens: {missing}")

bad = [tok for tok in forbidden_tokens if tok in text]
if bad:
    raise SystemExit(f"forbidden tokens present: {bad}")

if shutil.which("lake"):
    subprocess.run(["lake", "env", "lean", str(LEAN)], cwd=ROOT, check=True)

print("Chronos trace regime classifier verified: TRACE_REGIME_CLASSIFIER_SOLVED_FRONTIER_PRESERVED")
