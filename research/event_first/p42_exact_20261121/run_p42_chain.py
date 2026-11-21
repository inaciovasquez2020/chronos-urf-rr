#!/usr/bin/env python3
"""Reproducible sequential proof-chain replay for Chronos p_(4,2).

Runs on a checked-out PR source tree. No downloads, source writes, or
network calls. Exits at the first failure. Every script has a hard
time limit; a timeout is INCOMPLETE, never PASS. Requires SymPy,
mpmath, numpy, scipy for the indicated geometric and numerical audits.
"""
from pathlib import Path
import subprocess
import sys
import os

HERE=Path(__file__).resolve().parent
ORDER=(
    "chronos_p42_motif_reduction_audited.py",
    "chronos_p42_positive_dag_reduction.py",
    "chronos_p42_N_DAG_exact.py",
    "chronos_p42_coaxial_three_cone_spacetime.py",
    "chronos_p42_lorentz_three_cone_certificate.py",
    "chronos_p42_five_dimensional_B_reduction.py",
    "chronos_p42_four_dimensional_angular_kernel_audit.py",
    "chronos_p42_null_coordinate_kernel_audit.py",
    "chronos_p42_two_dimensional_J_kernel.py",
    "chronos_p42_exact_stdlib_certificate.py",
    "chronos_p42_exact_global_candidate.py",
)
for name in ORDER:
    p=HERE/name
    if not p.is_file():
        print("BLOCKED_MISSING_SOURCE :=",name,flush=True)
        sys.exit(2)
    try:
        result=subprocess.run(
            [sys.executable,"-B",str(p)],
            cwd=HERE,
            env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"},
            timeout=50,
            capture_output=True,
            text=True,
        )
    except subprocess.TimeoutExpired:
        print("INCOMPLETE_TIMEOUT :=",name,flush=True)
        sys.exit(3)
    if result.returncode:
        print("FAIL :=",name,"returncode",result.returncode,flush=True)
        print(result.stdout[-1200:])
        print(result.stderr[-1200:])
        sys.exit(result.returncode if result.returncode>0 else 1)
    print("PASS :=",name,flush=True)
print("CHAIN_REPLAY := PASS",len(ORDER),flush=True)
print("INDEPENDENT_GEOMETRIC_PROOF_REVIEW := OPEN",flush=True)
print("LEAN := NOT_RUN",flush=True)
