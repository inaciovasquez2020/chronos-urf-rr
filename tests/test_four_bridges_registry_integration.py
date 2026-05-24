import json
import re
from pathlib import Path


def test_four_bridges_registry_artifact_status_and_policy():
    data = json.loads(
        Path("artifacts/chronos/four_bridges_registry_integration_2026_05_24.json").read_text()
    )
    assert data["status"] == "FOUR_BRIDGES_REGISTRY_INTEGRATION_CONDITIONAL_EXTERNAL_ONLY"
    assert data["bridge_source"] == "FourBridgesSource"
    assert data["registry_class"] == "URF11BridgeRegistry"
    assert data["active_registry_instance_declared"] is False
    assert data["policy"]["admissible"] == "External 4bS certification supplies the URF11BridgeRegistry instance."
    for token in [
        "native active registry instance",
        "global bridge declaration",
        "macro or meta-program injection",
        "unconditional opaque-target closure without 4bS",
    ]:
        assert token in data["policy"]["rejected"]


def test_four_bridges_registry_claims_and_boundaries():
    data = json.loads(
        Path("artifacts/chronos/four_bridges_registry_integration_2026_05_24.json").read_text()
    )
    assert data["claims"]["r1_native_coherent_kernel_closed"] is True
    assert data["claims"]["r2_native_kernel_closed"] is True
    assert data["claims"]["r3_native_kernel_closed"] is True
    assert data["claims"]["four_bridges_registry_wired"] is True
    for key in [
        "active_registry_instance_declared",
        "unconditional_opaque_targets_closed",
        "non_factorisation_unconditional_closed",
        "chronos_rr_closed",
        "h4_1_fgl_closed",
        "p_vs_np_closed",
        "clay_problem_closed",
    ]:
        assert data["claims"][key] is False

    text = Path("docs/status/FOUR_BRIDGES_REGISTRY_INTEGRATION_2026_05_24.md").read_text()
    for token in data["boundary"]:
        assert token in text


def test_four_bridges_registry_lean_surface():
    text = Path("lean/Chronos/Frontier/FourBridgesRegistryIntegration.lean").read_text()
    for forbidden in [
        r"(?m)^\\s*axiom\\b",
        r"(?m)^\\s*opaque\\b",
        r"(?m)^\\s*instance\\b",
        r"\\bsorry\\b",
        r"\\badmit\\b",
    ]:
        assert not re.search(forbidden, text), forbidden

    for token in [
        "R1FinishedTheorem",
        "R2FinishedTheorem",
        "R3FinishedTheorem",
        "FourBridgesSource",
        "class URF11BridgeRegistry",
        "R1_from_4bS",
        "R2_from_4bS",
        "R3_from_4bS",
        "R4_from_4bS",
        "CompleteOpaqueSystem_registered",
        "FOUR_BRIDGES_REGISTRY_INTEGRATION_CONDITIONAL_EXTERNAL_ONLY",
    ]:
        assert token in text
