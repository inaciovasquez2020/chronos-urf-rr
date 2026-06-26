#!/usr/bin/env python3
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
artifact = root / "artifacts/external_validation/root_r1_interface_boundary_2026_06_26.json"
doc = root / "docs/status/ROOT_R1_INTERFACE_BOUNDARY_2026_06_26.md"
lean = root / "lean/Chronos/Frontier/R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceTarget.lean"
data = json.loads(artifact.read_text())
assert data["id"] == "ROOT_R1_INTERFACE_BOUNDARY_2026_06_26"
assert data["status"] == "BOUNDARY_CONFIRMED"
assert data["root_r1_interface"] == "R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceTarget"
assert data["lean_file"] == "lean/Chronos/Frontier/R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceTarget.lean"
assert "not NewsteinR1R2R3NativeBindingSupplied" in data["overarching_boundary"]
assert "not exists T : R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceTarget, True" in data["root_boundary"]
assert "does not construct the root R1 interface" in data["claim_boundary"]
assert "does not construct NewsteinR1R2R3NativeBindingSupplied" in data["claim_boundary"]
assert "does not close repository-native R1/R2/R3 promotion" in data["claim_boundary"]
doc_text = doc.read_text()
assert "R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceTarget" in doc_text
assert "BOUNDARY := not NewsteinR1R2R3NativeBindingSupplied" in doc_text
lean_text = lean.read_text()
assert "structure R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceTarget where" in lean_text
assert "def r1c_concrete_raw_endpoint_configuration_source_base_seed_carrier_source_input_target_from_source" in lean_text
print("ROOT_R1_INTERFACE_BOUNDARY_2026_06_26_OK")
