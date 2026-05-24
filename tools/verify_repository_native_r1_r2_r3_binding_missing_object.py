#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/RepositoryNativeR1R2R3BindingMissingObject.lean"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/repository_native_r1_r2_r3_binding_missing_object_2026_05_24.json"
STATUS = ROOT / "docs/status/REPOSITORY_NATIVE_R1_R2_R3_BINDING_MISSING_OBJECT_2026_05_24.md"

lean = LEAN.read_text()
root_import = ROOT_IMPORT.read_text()
artifact = json.loads(ARTIFACT.read_text())
status = STATUS.read_text()

for token in [
    "structure RepositoryNativeR1R2R3BindingSpec",
    "nativeWordSpec",
    "nativeEdgeSpec",
    "nativeFaceSpec",
    "nativeFiberSpec",
    "nativeTwoChainSpec",
    "nativeQuotientDataSpec",
    "r1MatchesOpenInputsRegistry",
    "r2MatchesOpenInputsRegistry",
    "r3MatchesOpenInputsRegistry",
    "def RepositoryNativeR1R2R3BindingSupplied",
    "theorem no_repository_native_R1_R2_R3_theorem_proof_without_binding",
]:
    assert token in lean, f"missing Lean token: {token}"

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

assert "import Chronos.Frontier.RepositoryNativeR1R2R3BindingMissingObject" in root_import
assert artifact["status"] == "MISSING_OBJECT_RECORDED_NO_THEOREM_PROMOTION"
assert artifact["missing_object"] == "RepositoryNativeR1R2R3BindingSpec"

for phrase in [
    "records missing repository-native R1/R2/R3 binding only",
    "does not prove LongChordExclusion",
    "does not prove DiameterSeparationFillingObstruction",
    "does not prove UniformLocalTypeCapacity",
    "does not prove NON_FACTORISATION",
    "does not prove Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove P vs NP",
    "does not prove any Clay problem",
]:
    assert phrase in artifact["boundary"], f"missing artifact boundary: {phrase}"
    assert phrase in status, f"missing status boundary: {phrase}"

print("repository-native R1/R2/R3 binding missing object verified.")
