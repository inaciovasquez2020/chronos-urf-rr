from pathlib import Path
import sys

REQUIRED = [
    "proofs/Chronos/conditional/H41_FINITE_PATCH_CORRELATION_LEMMA_2026_04.md",
    "proofs/Chronos/conditional/H41_FINITE_PATCH_OBJECTS_2026_04.md",
    "proofs/Chronos/conditional/H41_FINITE_PATCH_ORTHOGONALITY_TARGET_2026_04.md",
    "proofs/Chronos/conditional/H41_FINITE_PATCH_BASIS_REDUCTION_2026_04.md",
    "proofs/Chronos/conditional/H41_FINITE_PATCH_CORRELATION_TARGET_2026_04.md",
    "proofs/Chronos/conditional/H41_FINITE_PATCH_PROMOTION_2026_04.md",
    "proofs/Chronos/conditional/H41_FINITE_PATCH_FINAL_WALL_2026_04.md",
    "proofs/Chronos/conditional/H41_FINITE_PATCH_INDEX_2026_04.md",
    "proofs/Chronos/conditional/H41_FINITE_PATCH_EXEC_SUMMARY_2026_04.md",
    "proofs/Chronos/conditional/H41_FINITE_PATCH_STATUS_2026_04.yaml",
]

missing = [p for p in REQUIRED if not Path(p).exists()]
if missing:
    for p in missing:
        print(f"MISSING: {p}")
    sys.exit(1)

print("PASS: H4.1 finite-patch conditional chain present")
