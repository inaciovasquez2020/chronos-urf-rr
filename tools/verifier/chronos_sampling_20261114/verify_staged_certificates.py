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
    "exploratory/chronos_four_point_qmc_audit.py":
        "fff40406d8da87375d93700fc615848f4e6264970633ce35eaa83d3aa6cbdb47",
    "exploratory/chronos_overlap_qmc_check.py":
        "1d6de50683fd1c0741ce88c97f440e058b4217333555e9c6c02490691c71e346",
    "exploratory/chronos_overlap_rotational_reduction_20261114.py":
        "a3ba865adca3e979de76ce97b83291d5bae3b34603c7e70404782fc01d11f7ae",
    "primary/chronos_overlap_rigorous_lower_bound_20261114.py":
        "63daf938a9200683672703a5ec741f4946d41f5da18d7bc80173bc050965cc2a",
    "primary/chronos_lower_half_overlap_exact_20261114.py":
        "43465f88a981762c470a4a9f28553e87169ed59b3ad366e32946145787068f73",
    "supporting/chronos_overlap_prefix_audit_20261114.py":
        "cca24ced09b4954548645cd8c1e8b490428bd1977d4a5a534c470323a99859b1",
    "supporting/chronos_overlap_insertion_audit_20261114.py":
        "04291e6c71aa5226f87efe7986f0bd4100ca59923fde6e600370c379f27e3342",
    "supporting/chronos_four_event_bounds.py":
        "38e563c671a059c3eca567eb5816b23e7059797ea52366959789c9e834000409",
    "primary/chronos_four_point_chain_bounds_certificate.py":
        "6687c44b0949125cd4f62078b74749b863bbb453e2f9d9d0e403fbfdff6d79cd",
    "primary/chronos_four_point_mixed_moment_audit.py":
        "819def90550d3bc19074d2f4110683d3330d3242182c2f6c7ce423a55e65a7bb",
    "supporting/chronos_four_point_sharp_bounds.py":
        "492652e6dbb881a878ae6e0aee06d56ab135c39058172ad85b4060b96b7febe1",
}
for name, digest in EXPECTED.items():
    path = BASE / name
    if not path.is_file():
        raise SystemExit("MISSING_CERTIFICATE: " + name)
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit("HASH_MISMATCH: " + name)
    if name.startswith("exploratory/") or name == "primary/chronos_lower_half_overlap_exact_20261114.py":
        print("DEPENDENCY_GATED_NOT_RUN:", name)
        continue
    p = subprocess.run([sys.executable, "-B", str(path)],
                       capture_output=True, text=True, timeout=30)
    if p.returncode:
        print(p.stdout)
        print(p.stderr, file=sys.stderr)
        raise SystemExit("EXECUTION_FAILED: " + name)
    print("CERTIFICATE_PASS:", name)
print("BUNDLE_SOURCE_HASHES := 18/18 PASS")
print("STDLIB_EXACT_CERTIFICATES := 14/14 PASS")
print("DEPENDENCY_GATED_NUMERICAL_CERTIFICATES := 4 NOT_RUN")
print("FULL_BUNDLE_INTEGRATION := COMMITTED")
print("LEAN_VERIFIED := NOT_RUN")
print("MINKOWSKI_INFINITE_GROWTH_STABILITY := OPEN")
