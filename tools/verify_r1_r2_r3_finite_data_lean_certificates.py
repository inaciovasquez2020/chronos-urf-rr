#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/R1R2R3FiniteDataLeanCertificates.lean"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"
ART = ROOT / "artifacts/chronos/r1_r2_r3_finite_data_lean_certificates_2026_05_24.json"
DOC = ROOT / "docs/status/R1_R2_R3_FINITE_DATA_LEAN_CERTIFICATES_2026_05_24.md"

LEAN_TOKENS = [
    "def R1FiniteLongChordDataCertified : Prop :=",
    "theorem r1_finite_long_chord_data_certified",
    "def R2FiniteDiameterSeparationFillingDataCertified : Prop :=",
    "theorem r2_finite_diameter_separation_filling_data_certified",
    "def R3FiniteUniformLocalTypeCapacityDataCertified : Prop :=",
    "theorem r3_finite_uniform_local_type_capacity_data_certified",
    "def R1R2R3FiniteDataBundleCertified : Prop :=",
    "theorem r1_r2_r3_finite_data_bundle_certified",
    "def R1R2R3FiniteDataToNativeProofPromotionGap : Prop :="
]

BOUNDARY = [
    "LongChordExclusion",
    "DiameterSeparationFillingObstruction",
    "UniformLocalTypeCapacity",
    "native R1/R2/R3 instance",
    "NON_FACTORISATION",
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

    require("import Chronos.Frontier.R1R2R3FiniteDataLeanCertificates" in ROOT_IMPORT.read_text(),
            "missing root import")

    art = json.loads(ART.read_text())
    require(art["status"] == "FINITE_DATA_LEAN_CERTIFIED_PROMOTION_GAP_OPEN", "wrong status")
    require("r1_r2_r3_finite_data_bundle_certified" in art["closed_finite_certificates"], "missing bundle certificate")
    require("R1R2R3FiniteDataToNativeProofPromotionGap" in art["open_promotion_gaps"], "missing promotion gap")

    doc = DOC.read_text()
    for token in BOUNDARY:
        require(token in art["does_not_prove"], f"missing artifact boundary: {token}")
        require(token in doc, f"missing doc boundary: {token}")

    print("R1_R2_R3_FINITE_DATA_LEAN_CERTIFICATES_OK")

if __name__ == "__main__":
    main()
