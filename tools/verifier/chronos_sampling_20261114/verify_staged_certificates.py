#!/usr/bin/env python3
"""Fail-closed runner for the staged, exact, standard-library certificates.

This verifies source provenance and execution, not Lean/kernel proofs or
Minkowski infinite-growth sampling stability.
"""
import hashlib
import pathlib
import subprocess
import sys

BASE = pathlib.Path(__file__).resolve().parent
EXPECTED = {
    "primary/chronos_insertion_transfer_exact_20261114.py":
        "81393b324bff4c5871e5777314984f1866527dd6bb7e5a9d658df1d02b6cec12",
    "primary/chronos_overlap_decomposition_certificate.py":
        "8f31bba39ee4a2f176e18168e3240ea7fe4962d0d78d1b535fbc987b0d8a68f6",
    "primary/chronos_conditional_overlap_all_moments_20261114.py":
        "5465bbb74c17b77d9ef42967ca42230ddc688ea6138c2d0b6b42c86a5665f634",
    "supporting/chronos_comparable_pair_future_count_20261114.py":
        "5b7817920be647bcb067bed94d210e09c8bc74b6a85a026b64094d8d46235b82",
    "supporting/chronos_overlap_conditional_moment_audit_20261114.py":
        "08c95a6c77d9ce0f06de0f00458813b6656bfdc406c47d244511a12ee2feef24",
    "primary/chronos_symmetric_incomparable_overlap_exact_20261114.py":
        "e23a2a2c8962c983ee7fd452fbfe5f506978641ce51bf53d055f49561996363f",
    "primary/chronos_prefix_signed_insertion_exact_20261114.py":
        "0f6eb2209377ee38f8d6e1aeacea516d15285f96bd0d0e628f7df30dd610d50a",
    "primary/chronos_overlap_rigorous_lower_bound_20261114.py":
        "63daf938a9200683672703a5ec741f4946d41f5da18d7bc80173bc050965cc2a",
    "supporting/chronos_four_event_bounds.py":
        "38e563c671a059c3eca567eb5816b23e7059797ea52366959789c9e834000409",
}
for name, digest in EXPECTED.items():
    path = BASE / name
    if not path.is_file():
        raise SystemExit("MISSING_CERTIFICATE: " + name)
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit("HASH_MISMATCH: " + name)
    p = subprocess.run([sys.executable, "-B", str(path)],
                       capture_output=True, text=True, timeout=30)
    if p.returncode:
        print(p.stdout)
        print(p.stderr, file=sys.stderr)
        raise SystemExit("EXECUTION_FAILED: " + name)
    print("CERTIFICATE_PASS:", name)
print("STAGED_EXACT_CERTIFICATES := 9/9 PASS")
print("FULL_BUNDLE_INTEGRATION := INCOMPLETE")
print("LEAN_VERIFIED := NOT_RUN")
print("MINKOWSKI_INFINITE_GROWTH_STABILITY := OPEN")
