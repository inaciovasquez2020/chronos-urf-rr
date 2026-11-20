#!/usr/bin/env python3
"""Source-pinned, fail-closed November 15 Chronos certificate replay.

Checks all 15 original Python files and 9 mathematical notes byte-for-byte.
Runs 12 dependency-free certificates. The other three are preserved with
explicit dependency gates, not silently credited as GitHub CI passes.
Execution is finite evidence and does not establish Minkowski limit theorems.
"""
import hashlib
import pathlib
import subprocess
import sys

BASE = pathlib.Path(__file__).resolve().parent
DOCS = BASE.parents[2] / "docs/research/chronos_sampling_20261115"
CHECKS = {
 "exact/chronos_first_choice_fishburn_sharp_audit_20261115.py": "c38a201973af31457a71ac1cfb3d214e6bd767f46829b693ce26f80c24e56c54",
 "exact/chronos_double_limit_vs_two_prefix_certificate_20261115.py": "e6deb3e5582efb627155203b4f977098fdfdec85acb5bc6a10a4a9eac3e7c73e",
 "exact/chronos_eight_extremal_posets_refined_exact_20261115.py": "c7d8ea397a239684649b2fc606b6586812ded6cadc990bd00e3667f4090cac19",
 "exact/chronos_exact_N_K_reduction_certificate_20261115.py": "addacfed087daa386917dfaae41fec97298829bd011310bf9db4c6219125b4b1",
 "exact/chronos_overlap_spectral_exact_bounds_20261115.py": "a71bcb40c7723af510421110b4cf788b29212ddd757fb9d6192ee8decfe65ff3",
 "exact/chronos_matching_global_density_counterexample_20261115.py": "dcbe5fed655672e3c8b0492a16cb2493807320b5b3e1514458a4ae01abd52002",
 "exact/chronos_overlap_5mode_rigorous_20261115.py": "180a6746dd7baafb6e98afafcfc57f168d8e4a769e9d6a494d1bb49ce5c3bda0",
 "exact/chronos_predecessor_concentration_geometry_audit_20261115.py": "aeb2c12c5eac988ceff9c1c96cdc7b307ac61d7cb2fc0005272ba2ca7d62ed6c",
 "exact/chronos_overlap_exact_l0_independent_audit_20261115.py": "240219e2b5dc364ad7ddc0db2e36739525f9f182f12ba73e0e9e564d6e3e99db",
 "exact/chronos_ideal_weight_scaling_certificate_20261115.py": "c61cfa7d4e843d0266b91c280e4ba7aef55ed18bac8e14c8d47ffda5b3aca67a",
 "exploratory/chronos_exact_prefix_growth_finite_sweep_20261115.py": "befcaf8f1ad1b7b9625390c3c1231736f46fcec25426ca4b13a9d510079fd314",
 "exact/chronos_extension_weight_nonidentifiability_audit_20261115.py": "69d9c7713901e717f411815d17c93f366e85cb504d6051f444352982e9cc2188",
 "exact/chronos_full_prefix_limit_range_certificate_20261115.py": "e935a455588c0d1a668a24188e24271cf478bee64379e16aaf51bddb198a5845",
 "exact/chronos_matching_all_fixed_predecessor_counts_counterexample_20261115.py": "245506f93f399937bfab8dbb23052ce6ca439c840ab23edb6e0ac3106ed714df",
 "exploratory/chronos_4d_qmc_N_K_overlap_20261115.py": "169e3f71de99c00b9eaf3102ad1d71b11e700d91fb89db1fac629617be4079ec",
}
DOC_CHECKS = {
 "CHRONOS_EXTENSION_WEIGHT_NONIDENTIFIABILITY_20261115.md": "932e12e8c81fcf78447bbd55b732bcbafac04bd9f403051b79f97dfa8888c3c1",
 "CHRONOS_GEOMETRIC_AND_GROWTH_AUDIT_20261115.md": "39656d29c7699ddef8ae938786962d58dc90ec6b6581b311e68efd4c12aac71a",
 "chronos_predecessor_count_concentration_20261115.md": "758f2401fee9bd0b7249b3853b97b2642f1e682068c53bccf9dc1d0597b4b86f",
 "CHRONOS_FIRST_CHOICE_SUCCESSOR_SANDWICH_20261115.md": "8196fbc022473ae562b3b64560305c6907fda1a3f2f462d8856f43de4dd5e50d",
 "CHRONOS_FULL_PREFIX_FISHBURN_TRANSFER_20261115.md": "0af1d3512c2ef3b299be2e59ac44c6e24deacb7361b4668733a11e4eae75241b",
 "CHRONOS_PREFIX_NULL_LAYER_THEOREM_20261115.md": "80ccb983203ede184cb2d7669cb0d1061201f57cb96b907a2f250a05706550a4",
 "CHRONOS_PREFIX_WEIGHT_BOUNDARY_20261115.md": "7edb47619537e889b58071ae187d5e31eafb1c8fafc977a910149bd0152f70fa",
 "CHRONOS_TIP_FIRST_SUCCESSOR_RANK_AUDIT_20261115.md": "06f40ab4e1fcb93efe5b760119f15a77f9cecb1b87189bc145a907a3b4d8a4a9",
 "CHRONOS_TIP_POISSON_LOCAL_LIMIT_20261115.md": "8423ecf539ef7bf3dc2da2f275e754d8c2757a8b44a12be6087714bc589d47f3",
}
DEPENDENCY_GATED = {
 "exact/chronos_exact_N_K_reduction_certificate_20261115.py": "sympy",
 "exploratory/chronos_exact_prefix_growth_finite_sweep_20261115.py": "numpy",
 "exploratory/chronos_4d_qmc_N_K_overlap_20261115.py": "numpy/scipy",
}
def check_file(path, digest):
    if not path.is_file():
        raise SystemExit("MISSING: " + str(path))
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    if got != digest:
        raise SystemExit("SHA256_MISMATCH: " + str(path))

for name,digest in CHECKS.items():
    check_file(BASE/name, digest)
for name,digest in DOC_CHECKS.items():
    check_file(DOCS/name, digest)

passed = 0
for name in CHECKS:
    if name in DEPENDENCY_GATED:
        print("DEPENDENCY_GATED_NOT_RUN:", name, DEPENDENCY_GATED[name])
        continue
    try:
        result = subprocess.run([sys.executable,"-E","-B",str(BASE/name)],
                                capture_output=True,text=True,timeout=75)
    except subprocess.TimeoutExpired:
        raise SystemExit("INCOMPLETE_TIMEOUT: " + name)
    if result.returncode:
        print(result.stdout)
        print(result.stderr,file=sys.stderr)
        raise SystemExit("CERTIFICATE_FAILED: " + name)
    print("CERTIFICATE_PASS:", name)
    passed += 1

assert len(CHECKS)==15 and len(DOC_CHECKS)==9 and len(DEPENDENCY_GATED)==3
assert passed==12
print("SOURCE_HASHES := 24/24 PASS")
print("STDLIB_CERTIFICATE_REPLAY := 12/12 PASS")
print("DEPENDENCY_GATED := 3 NOT_RUN")
print("MINKOWSKI_P42 := OPEN")
print("INFINITE_GROWTH_DOUBLE_LIMIT := OPEN")
print("LEAN_VERIFIED := NOT_RUN")
