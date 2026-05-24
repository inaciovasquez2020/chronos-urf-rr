#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/R1R2R3NonFactorisationPromotionLock.lean"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/r1_r2_r3_non_factorisation_promotion_lock_2026_05_24.json"
STATUS = ROOT / "docs/status/R1_R2_R3_NON_FACTORISATION_PROMOTION_LOCK_2026_05_24.md"

lean = LEAN.read_text()
root_import = ROOT_IMPORT.read_text()
artifact = json.loads(ARTIFACT.read_text())
status = STATUS.read_text()

required_lean_tokens = [
    "structure LongChordExclusionSubsteps",
    "R1a_trivialFacesAvoidLongChords",
    "R1b_linearCombinationsCannotCreateLongChords",
    "R1c_maximalSeparationForbidsTrivialLongChord",
    "def LongChordExclusionClosed",
    "theorem LongChordExclusion_from_R1a_R1b_R1c",
    "structure DiameterSeparationFillingObstructionSubsteps",
    "R2a_boundedFillingLocalizesToRootedRegion",
    "R2b_distinctFiberSupportsCannotBeJoinedByBoundedTwoChain",
    "R2c_boundedFillingForcesForbiddenTwistedClassIdentification",
    "R2d_geometricSeparationImpliesAlgebraicInjectivity",
    "def DiameterSeparationFillingObstructionClosed",
    "theorem DiameterSeparationFillingObstruction_from_R2a_R2b_R2c_R2d",
    "structure UniformLocalTypeCapacitySubsteps",
    "R3a_boundedLocalTypeFactorizationFiniteStateSpace",
    "R3b_finiteStateFactorizationBoundsImageDimension",
    "R3c_equalLocalTypeDataGivesEqualQuotientData",
    "R3d_uniformDimensionBoundExtracted",
    "def UniformLocalTypeCapacityClosed",
    "theorem UniformLocalTypeCapacity_from_R3a_R3b_R3c_R3d",
    "structure R1R2R3NonFactorisationInputs",
    "theorem R1_R2_R3_TO_NON_FACTORISATION",
    "structure R1R2R3TheoremInputs",
    "def ChronosRRPromotionAllowed",
    "def H41FGLPromotionAllowed",
    "theorem no_nonfactorisation_promotion_without_R1_R2_R3",
    "theorem no_chronos_rr_promotion_without_R1",
    "theorem no_chronos_rr_promotion_without_R2",
    "theorem no_chronos_rr_promotion_without_R3",
    "theorem no_h41_fgl_promotion_without_R1",
    "theorem no_h41_fgl_promotion_without_R2",
    "theorem no_h41_fgl_promotion_without_R3",
]
for token in required_lean_tokens:
    assert token in lean, f"missing Lean token: {token}"

for forbidden in [
    "axiom ",
    "admit",
    "sorry",
    "theorem ChronosRR",
    "theorem H41FGL",
    "theorem PvsNP",
    "theorem Clay",
    "proved NON_FACTORISATION",
    "proved Chronos-RR",
    "proved H4.1/FGL",
]:
    assert forbidden not in lean, f"forbidden Lean token present: {forbidden}"

assert "import Chronos.Frontier.R1R2R3NonFactorisationPromotionLock" in root_import

assert artifact["status"] == "CONDITIONAL_INTERFACE_AND_NO_PROMOTION_LOCK_ONLY"
assert artifact["conditional_chain"] == "R1_R2_R3_TO_NON_FACTORISATION"
for key in ["R1", "R2", "R3"]:
    assert key in artifact["formalized_substeps"], f"missing artifact key: {key}"

for phrase in [
    "does not prove LongChordExclusion",
    "does not prove DiameterSeparationFillingObstruction",
    "does not prove UniformLocalTypeCapacity",
    "does not prove NON_FACTORISATION",
    "does not prove Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove P vs NP",
    "does not prove any Clay problem",
]:
    assert phrase in artifact["boundary"], f"missing artifact boundary phrase: {phrase}"
    assert phrase in status, f"missing status boundary phrase: {phrase}"

print("R1/R2/R3 non-factorisation promotion lock verified.")
