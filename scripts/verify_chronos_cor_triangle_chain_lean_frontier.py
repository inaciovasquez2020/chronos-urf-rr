#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "chronos" / "Frontier" / "CORTriangleChainFrontier.lean"
DOC = ROOT / "docs" / "status" / "CHRONOS_COR_TRIANGLE_CHAIN_LEAN_FRONTIER_2026_05_02.md"

REQUIRED_LEAN = [
    "abbrev TriangleChainGraph",
    "def triangleChainGraph",
    "opaque CertifiedObstructionRankZero",
    "axiom triangleChain_COR0_eq_blocks",
    "theorem triangleChain_COR0_linear_lower_bound",
]

REQUIRED_DOC = [
    "LEAN THEOREM-FRONTIER SKELETON / AXIOM-LEVEL TARGET",
    "triangleChain_COR0_eq_blocks",
    "triangleChain_COR0_linear_lower_bound",
    "This is a Lean theorem-frontier skeleton only.",
    "It does not prove finite-to-general lift.",
    "It does not prove locality-to-depth bridge.",
    "It does not prove theorem-level Chronos closure.",
    "It does not assert a Chronos closure theorem.",
    "It does not solve P vs NP.",
]

FORBIDDEN = [
    "finite-to-general lift is proved",
    "locality-to-depth bridge is proved",
    "theorem-level Chronos closure is proved",
    "unconditional Chronos theorem is proved",
    "P vs NP is solved",
]

def main() -> None:
    lean = LEAN.read_text()
    doc = DOC.read_text()

    missing_lean = [token for token in REQUIRED_LEAN if token not in lean]
    missing_doc = [token for token in REQUIRED_DOC if token not in doc]
    forbidden = [token for token in FORBIDDEN if token in lean or token in doc]

    if missing_lean:
        raise SystemExit(f"missing Lean tokens: {missing_lean}")
    if missing_doc:
        raise SystemExit(f"missing doc tokens: {missing_doc}")
    if forbidden:
        raise SystemExit(f"forbidden overclaim tokens: {forbidden}")

    lake = shutil.which("lake")
    if lake is not None:
        subprocess.run([lake, "env", "lean", str(LEAN)], check=True)

    print("Chronos COR triangle-chain Lean frontier verification OK.")

if __name__ == "__main__":
    main()
