from pathlib import Path
import json
import re

lean = Path("lean/Chronos/Frontier/FourBridgesRegistryIntegration.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/four_bridges_registry_integration_2026_05_24.json").read_text())
doc = Path("docs/status/FOUR_BRIDGES_REGISTRY_INTEGRATION_2026_05_24.md").read_text()
root = Path("lean/Chronos.lean").read_text()

for forbidden in [
    r"(?m)^\s*axiom\b",
    r"(?m)^\s*opaque\b",
    r"(?m)^\s*instance\b",
    r"\bsorry\b",
    r"\badmit\b",
]:
    assert not re.search(forbidden, lean), forbidden

required_lean = [
    "R1FinishedTheorem",
    "R1FinishedTheorem_proved",
    "R2FinishedTheorem",
    "R2FinishedTheorem_proved",
    "R3FinishedTheorem",
    "R3FinishedTheorem_proved",
    "FourBridgesSource",
    "FourBridgesSourceStatus",
    "R1_from_4bS",
    "R2_from_4bS",
    "R3_from_4bS",
    "RepositoryNativeR1R2R3InstanceTarget_from_4bS",
    "R4_from_4bS",
    "CompleteOpaqueSystem_conditional_on_4bS",
    "class URF11BridgeRegistry",
    "R1_registered_extraction",
    "R2_registered_extraction",
    "R3_registered_extraction",
    "R4_registered_extraction",
    "CompleteOpaqueSystem_registered",
    "FOUR_BRIDGES_REGISTRY_INTEGRATION_CONDITIONAL_EXTERNAL_ONLY",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "FOUR_BRIDGES_REGISTRY_INTEGRATION_CONDITIONAL_EXTERNAL_ONLY"
assert artifact["bridge_source"] == "FourBridgesSource"
assert artifact["registry_class"] == "URF11BridgeRegistry"
assert artifact["active_registry_instance_declared"] is False
assert artifact["policy"]["admissible"] == "External 4bS certification supplies the URF11BridgeRegistry instance."

for claim in [
    "r1_native_coherent_kernel_closed",
    "r2_native_kernel_closed",
    "r3_native_kernel_closed",
    "four_bridges_registry_wired",
]:
    assert artifact["claims"][claim] is True, claim

for claim in [
    "active_registry_instance_declared",
    "unconditional_opaque_targets_closed",
    "non_factorisation_unconditional_closed",
    "chronos_rr_closed",
    "h4_1_fgl_closed",
    "p_vs_np_closed",
    "clay_problem_closed",
]:
    assert artifact["claims"][claim] is False, claim

for token in artifact["native_finished_theorems"]:
    assert token in lean, token
    assert token in doc, token

for token in artifact["extraction_surfaces"]:
    assert token in lean, token
    assert token in doc, token

for boundary in artifact["boundary"]:
    assert boundary in doc, boundary

assert "import Chronos.Frontier.FourBridgesRegistryIntegration" in root

print("Four Bridges Source registry integration verified.")
