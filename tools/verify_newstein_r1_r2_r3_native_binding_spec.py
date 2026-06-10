#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/NewsteinR1R2R3NativeBindingSpec.lean"
DOC = ROOT / "docs/math/NEWSTEIN_R1_R2_R3_NATIVE_BINDING_SPEC.md"
STATUS = ROOT / "docs/status/NEWSTEIN_R1_R2_R3_NATIVE_BINDING_SPEC_2026_05_24.md"
ARTIFACT = ROOT / "artifacts/chronos/newstein_r1_r2_r3_native_binding_spec_2026_05_24.json"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

lean = LEAN.read_text()
doc = DOC.read_text()
status = STATUS.read_text()
artifact = json.loads(ARTIFACT.read_text())
root_import = ROOT_IMPORT.read_text()

required_lean = [
    "structure NewsteinR1R2R3NativeBindingSpec",
    "nativeR1Data : R1SemanticData",
    "nativeR2Data : R2SemanticData",
    "nativeR3Data : R3SemanticData",
    "r1Correct : R1LongChordExclusionTheorem nativeR1Data",
    "r2Correct : R2DiameterSeparationFillingObstructionTheorem nativeR2Data",
    "r3Correct : R3UniformLocalTypeCapacityTheorem nativeR3Data",
    "def NewsteinR1R2R3NativeBindingSupplied",
    "def RepositoryNativeR1R2R3TheoremsClosed",
    "theorem repository_native_R1_R2_R3_theorems_from_binding_spec",
    "def RepositoryNativeNonFactorisationPromotionAllowed",
    "theorem repository_native_nonfactorisation_promotion_from_binding_spec",
    "def RepositoryNativeChronosRRPromotionAllowed",
    "def RepositoryNativeH41FGLPromotionAllowed",
    "theorem no_repository_native_promotion_without_binding_supplied",
    "theorem no_repository_native_chronos_rr_promotion_without_binding_supplied",
    "theorem no_repository_native_h41_fgl_promotion_without_binding_supplied",
]
for token in required_lean:
    assert token in lean, f"missing Lean token: {token}"

for token in [
    "W^{\\text{triv}}",
    "\\Phi_2^{\\text{triv}}",
    "\\partial\\tau",
    "\\text{supp}(w)",
    "e_1, e_2",
    "\\text{FiberClass}",
    "Z_1 / W^{\\text{glob}}",
    "\\text{TwoChain}",
    "\\text{diam}",
    "\\text{LocalType}(r, k, \\Delta)",
    "C(r, k, \\Delta)",
]:
    assert token in doc, f"missing doc token: {token}"

assert artifact["status"] == "SPECIFICATION_ONLY_NO_NATIVE_INSTANCE"
assert artifact["lean_object"] in {
    "RepositoryNativeR1R2R3BindingSpec",
    "NewsteinR1R2R3NativeBindingSpec",
}
assert "import Chronos.Frontier.NewsteinR1R2R3NativeBindingSpec" in root_import

for phrase in [
    "specification only",
    "does not construct NewsteinR1R2R3NativeBindingSpec",
    "does not prove LongChordExclusion",
    "does not prove DiameterSeparationFillingObstruction",
    "does not prove UniformLocalTypeCapacity",
    "does not prove NON_FACTORISATION",
    "does not prove Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove P vs NP",
    "does not prove any Clay problem",
]:
    assert phrase in artifact["boundary"] or phrase.replace("NewsteinR1R2R3NativeBindingSpec", "RepositoryNativeR1R2R3BindingSpec") in artifact["boundary"], f"missing artifact boundary: {phrase}"
    assert phrase in status or phrase.replace("NewsteinR1R2R3NativeBindingSpec", "RepositoryNativeR1R2R3BindingSpec") in status, f"missing status boundary: {phrase}"

for forbidden in [
    "axiom ",
    "admit",
    "sorry",
    "proved LongChordExclusion",
    "proved DiameterSeparationFillingObstruction",
    "proved UniformLocalTypeCapacity",
    "proved NON_FACTORISATION",
    "proved Chronos-RR",
    "proved H4.1/FGL",
    "P vs NP proved",
    "Clay problem solved",
]:
    assert forbidden not in lean, f"forbidden Lean token: {forbidden}"

print("Newstein R1/R2/R3 native binding spec verified.")
