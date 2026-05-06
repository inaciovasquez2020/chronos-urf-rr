#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "chronos" / "Certified" / "RepositoryNativeCertifiedDepth.lean"
STATUS = ROOT / "docs" / "status" / "CHRONOS_REPOSITORY_NATIVE_CERTIFIED_DEPTH_2026_05_06.md"

text = LEAN.read_text()
status = STATUS.read_text()

for banned in ["import Mathlib", "by sorry", "admit", "axiom ", "linarith", "omega", "norm_cast", "exact_mod_cast", "ℚ"]:
    if banned in text:
        print(f"Forbidden token found: {banned}")
        sys.exit(1)

required_lean = [
    "structure CertifiedObstructionConstants",
    "structure RepositoryNativeCarrierIso",
    "structure RepositoryNativeCertificate",
    "def EmbedSearchFamilyRepositoryNative",
    "def RepositoryNativeDepth",
    "theorem RepositoryNativeDepthLowerBound",
    "theorem ObstructionConstantsPreserved",
    "theorem EmbedSearchFamilyPreservesObstructions",
    "theorem RepositoryNativeCertifiedDepthLowerBound",
    "def RepositoryNativeDepthBridgeHypothesis",
    "theorem repositoryNativeDepthBridgeInstance",
    "theorem no_closure_claimed",
    "I.depthAnnotation",
    "I.depthMinimum",
    "I.backward n x.query",
    "I.right_inv n x.query",
    "hk : k = n ∨ k ≤ n",
    "hrn : n ≤ r",
]

required_status = [
    "REPOSITORY_NATIVE_DEPTH_BRIDGE_FORMALIZED",
    "`hk : k = n ∨ k ≤ n`",
    "`hrn : n ≤ r`",
    "`FRONTIER_OPEN` is preserved",
    "Does not assert P vs NP closure",
    "does not import `Mathlib`",
]

missing = [s for s in required_lean if s not in text]
if missing:
    print("Missing Lean tokens:")
    for item in missing:
        print(f"  - {item}")
    sys.exit(1)

missing_status = [s for s in required_status if s not in status]
if missing_status:
    print("Missing status tokens:")
    for item in missing_status:
        print(f"  - {item}")
    sys.exit(1)

subprocess.run(["lake", "env", "lean", str(LEAN)], cwd=ROOT, check=True)

print("Chronos repository-native certified depth verified: REPOSITORY_NATIVE_DEPTH_BRIDGE_FORMALIZED")
