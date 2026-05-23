#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean_file = ROOT / "lean/Chronos/Frontier/GravityClosureKernelTarget.lean"
artifact_file = ROOT / "artifacts/chronos/gravity_closure_kernel_target_2026_05_22.json"
doc_file = ROOT / "docs/status/GRAVITY_CLOSURE_KERNEL_TARGET_2026_05_22.md"
chronos_file = ROOT / "lean/Chronos.lean"

lean = lean_file.read_text()
artifact = json.loads(artifact_file.read_text())
doc = doc_file.read_text()
chronos = chronos_file.read_text()

assert "import Chronos.Frontier.GravityClosureKernelTarget" in chronos
assert "structure NonSymmetricEinsteinMatterBootstrapKernel" in lean
assert "theorem collapseGate_from_bootstrapKernel" in lean
assert "def GravityClosureKernelTarget : Prop" in lean
assert "sourceLevelEvidence_does_not_construct_kernel" in lean

assert artifact["status"] == "KERNEL_TARGET_ONLY_GRAVITY_CLOSURE_OPEN"
assert artifact["closed_result"] == "collapseGate_from_bootstrapKernel"
assert artifact["open_target"] == "GravityClosureKernelTarget"
assert "NonSymmetricEinsteinMatterBootstrapKernel" in artifact["missing_object"]

for token in [
    "gravity closure",
    "cosmic censorship",
    "hoop conjecture",
    "four-dimensional collapse theorem",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in artifact["does_not_prove"]
    assert token in doc

print("Gravity closure kernel target verification OK.")
print(f"Status: {artifact['status']}")
print(f"Open target: {artifact['open_target']}")
print(f"Missing object: {artifact['missing_object']}")
