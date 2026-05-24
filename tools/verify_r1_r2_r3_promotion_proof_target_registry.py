#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/R1R2R3PromotionProofTargetRegistry.lean"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"
ART = ROOT / "artifacts/chronos/r1_r2_r3_promotion_proof_target_registry_2026_05_24.json"
DOC = ROOT / "docs/status/R1_R2_R3_PROMOTION_PROOF_TARGET_REGISTRY_2026_05_24.md"

LEAN_TOKENS = [
    "def R1PromotionProofTarget : Prop :=",
    "def R2PromotionProofTarget : Prop :=",
    "def R3PromotionProofTarget : Prop :=",
    "def NonFactorisationBridgeProofTarget : Prop :=",
    "def R1R2R3PromotionProofTargetRegistry : Prop :=",
    "def R1R2R3PromotionProofTargetRegistryOpen : Prop :=",
    "def R1PromotionProofTargetStatus : String := \"OPEN\"",
    "def R2PromotionProofTargetStatus : String := \"OPEN\"",
    "def R3PromotionProofTargetStatus : String := \"OPEN\"",
    "def NonFactorisationBridgeProofTargetStatus : String := \"OPEN\""
]

OPEN_TARGETS = [
    "R1PromotionProofTarget",
    "R2PromotionProofTarget",
    "R3PromotionProofTarget",
    "NonFactorisationBridgeProofTarget"
]

BOUNDARY = [
    "R1PromotionProofTarget",
    "R2PromotionProofTarget",
    "R3PromotionProofTarget",
    "NonFactorisationBridgeProofTarget",
    "LongChordExclusion",
    "DiameterSeparationFillingObstruction",
    "UniformLocalTypeCapacity",
    "native R1/R2/R3 instance unconditionally",
    "NON_FACTORISATION unconditionally",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem"
]

def require(cond, msg):
    if not cond:
        raise AssertionError(msg)

def main():
    for path in [LEAN, ROOT_IMPORT, ART, DOC]:
        require(path.exists(), f"missing {path}")

    lean = LEAN.read_text()
    for token in LEAN_TOKENS:
        require(token in lean, f"missing Lean token: {token}")

    require("import Chronos.Frontier.R1R2R3PromotionProofTargetRegistry" in ROOT_IMPORT.read_text(),
            "missing root import")

    data = json.loads(ART.read_text())
    require(data["status"] == "PROOF_TARGET_REGISTRY_OPEN", "wrong status")
    require(data["registry"] == "R1R2R3PromotionProofTargetRegistry", "wrong registry")
    require(data["open_marker"] == "R1R2R3PromotionProofTargetRegistryOpen", "wrong open marker")

    names = [item["name"] for item in data["open_targets"]]
    require(names == OPEN_TARGETS, f"wrong open target list: {names}")
    for item in data["open_targets"]:
        require(item["status"] == "OPEN", f"{item['name']} not OPEN")

    doc = DOC.read_text()
    for token in BOUNDARY:
        require(token in data["does_not_prove"], f"missing artifact boundary: {token}")
        require(token in doc, f"missing doc boundary: {token}")

    print("R1_R2_R3_PROMOTION_PROOF_TARGET_REGISTRY_OK")

if __name__ == "__main__":
    main()
