#!/usr/bin/env python3
from pathlib import Path

allowed = {
    "docs/status/WHOLE_URF_FRONTIER_POINTER.md",
    "docs/status/URF_FRONTIER_POINTER_REGISTRY_V1.json",
    "tests/test_whole_urf_frontier_pointer_doc.py",
    "tests/test_chronos_frontier_sync.py",
    "tests/test_urf_frontier_pointer_registry_v1.py",
    "tests/test_urf_frontier_projection_check.py",
    "tests/test_urf_frontier_pointer_registry_schema_lock.py",
    "scripts/check_urf_frontier_projection.py",
    "scripts/check_urf_frontier_pointer_registry_schema_lock.py",
    "scripts/check_generated_pointer_parity.py",
}

needles = [
    "URF_REMAINING_FRONTIER_CANONICAL.md",
    "URF_FRONTIER_REGISTRY_V1.json",
    "whole-URF residual frontier",
    "URF residual frontier",
    "witness_family_boundary",
]

hits = []
for p in Path(".").rglob("*"):
    if not p.is_file():
        continue
    if ".git/" in str(p):
        continue
    if p.parts and p.parts[0] == ".lake":
        continue
    if p.parts and p.parts[0] == "build":
        continue
    try:
        s = p.read_text()
    except Exception:
        continue
    for needle in needles:
        if needle in s:
            rel = p.as_posix()
            if rel == "scripts/check_urf_frontier_zero_divergence.py":
                continue
            if rel not in allowed:
                hits.append((rel, needle))

assert not hits, hits
print("urf-frontier-zero-divergence: PASS")
