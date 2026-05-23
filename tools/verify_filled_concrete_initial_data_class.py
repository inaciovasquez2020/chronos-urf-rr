#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/filled_concrete_initial_data_class_2026_05_23.json"
doc = ROOT / "docs/status/FILLED_CONCRETE_INITIAL_DATA_CLASS_2026_05_23.md"
lean = ROOT / "lean/Chronos/Frontier/FilledConcreteInitialDataClass.lean"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
assert data["id"] == "FILLED_CONCRETE_INITIAL_DATA_CLASS"
assert data["status"] == "FILLED_CONCRETE_INITIAL_DATA_CLASS_ONLY_NO_ANALYTIC_ESTIMATE_PROOF"
assert data["current_frontier_before"] == "CANDIDATE_PACKET_ONLY_NO_ANALYTIC_ESTIMATE_PROOF"
assert data["object_type"] == "constructor_input_surface"
fields = data["filled_fields"]
required_true = [
    "compact_support",
    "finite_energy",
    "constraint_compatible",
    "matter_compatible",
    "nonsymmetric_seed_present",
    "bootstrap_slab_compatible",
    "boundary_conditions_specified",
]
assert fields["spatial_dimension"] == 3
assert fields["regularity_index"] >= 8
for key in required_true:
    assert fields[key] is True

required_boundaries = [
    "analytic estimate proof",
    "SixFieldAnalyticPackageHypothesis proof",
    "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage proof",
    "Einstein-matter well-posedness",
    "non-symmetric persistence",
    "matter-coupling control",
    "concentration transport",
    "collapse-gate trigger",
    "cosmic censorship",
    "hoop conjecture",
    "gravity closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]
for token in required_boundaries:
    assert token in data["does_not_prove"]
    assert token in doc.read_text()

lean_text = lean.read_text()
assert "structure FilledConcreteInitialDataClass" in lean_text
assert "canonicalFilledConcreteInitialDataClass_isFilled" in lean_text
assert "filledConcreteInitialDataClass_boundary_noAnalyticEstimateProof" in lean_text
assert "import Chronos.Frontier.FilledConcreteInitialDataClass" in root_import.read_text()

print("Filled concrete initial data class verification OK.")
print("Status:", data["status"])
print("Next admissible object:", data["next_admissible_object"])
