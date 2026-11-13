#!/usr/bin/env python3
"""Fail-closed exact-HEAD runner for the four finite CSG certificates (Python >=3.9)."""
from pathlib import Path
from hashlib import sha256
import subprocess
import sys

if not __debug__:
    raise SystemExit("FAIL: Python assertions disabled")
ROOT = Path(__file__).resolve().parent
CASES = (
    ("rr_csg_common_four_exact_existence_py39.py", "90e98f44fe874258c6089fbcf0054676a844b7e056c354a50f76dafb1d952319", "EXISTENCE_AND_LOCAL_UNIQUENESS := PROVED_BY_CONTRACTION"),
    ("rr_csg_five_event_nonextension.py", "4a897d7171220caee4f6fed0b2267d2c10d15ec6b914c1f93f9563c981e66ca3", "FINITE_FIVE_EVENT_OBSTRUCTION := PROVED_CONDITIONALLY_ON_FOUR_EVENT_CERTIFICATE"),
    ("rr_csg_global_uniqueness.py", "179ee9e148bf0ea4c68a30709d1b6a7445966e73ea49d24bb15c1a07306eab03", "STURM_AND_INTERVAL_SIGNS := PASS"),
    ("rr_csg_elimination_ideal_audit_py39.py", "a995f13622a7ebee61dfb9a931c201c026d66aa4caf8456a0f46690ee13942e0", "GROEBNER_IDEAL_EQUIVALENCE := PASS"),
)
for name, expected, marker in CASES:
    path = ROOT / name
    if not path.is_file():
        raise SystemExit("FAIL: missing " + name)
    digest = sha256(path.read_bytes()).hexdigest()
    if digest != expected:
        raise SystemExit("FAIL: source hash mismatch " + name + " " + digest)
    try:
        p = subprocess.run([sys.executable, "-B", str(path)], text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=120, check=False, cwd=str(ROOT))
    except subprocess.TimeoutExpired:
        raise SystemExit("INCOMPLETE_TIMEOUT: " + name)
    if p.returncode or marker not in p.stdout:
        print(p.stdout[-3000:])
        print(p.stderr[-3000:], file=sys.stderr)
        raise SystemExit("FAIL: " + name + " returncode " + str(p.returncode))
    print("PASS: " + name + " SHA256=" + digest)
print("FINITE_CSG_CERTIFICATES := COMPUTATION_PASS")
print("LEAN_VERIFIED := NOT_RUN")
print("PHYSICAL_CONTINUUM_THEOREM := OPEN")
