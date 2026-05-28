#!/usr/bin/env python3
import json
from pathlib import Path

lean = Path("lean/Chronos/Frontier/PartitionedBudgetPhysicalDetectorGateBound.lean")
artifact = Path("artifacts/chronos/partitioned_budget_physical_detector_gate_bound_2026_05_28.json")
doc = Path("docs/status/PARTITIONED_BUDGET_PHYSICAL_DETECTOR_GATE_BOUND_2026_05_28.md")

for path in [lean, artifact, doc]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "structure PartitionedPhysicalDetectorBudgetCertificate",
    "reading_le_budget",
    "budget_le_partition",
    "partitionedBudgetCertificate_implies_gate_bound",
    "partitionedBudgetCertificate_to_admissible",
    "partitionedBudgetCertificate_feeds_restrictedFiniteDetectorGate_derived",
    "twoDetectorExample_closes_gate"
]

for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

if data.get("status") != "DERIVED_GATE_BOUND_FROM_PARTITIONED_BUDGET_CERTIFICATE":
    raise SystemExit("bad artifact status")

if "PartitionedPhysicalDetectorBudgetCertificate" not in data.get("conditional_on", []):
    raise SystemExit("missing certificate condition")

for theorem in [
    "partitionedBudgetCertificate_implies_gate_bound",
    "partitionedBudgetCertificate_to_admissible",
    "partitionedBudgetCertificate_feeds_restrictedFiniteDetectorGate_derived",
    "twoDetectorExample_closes_gate"
]:
    if theorem not in data.get("closed_theorems", []):
        raise SystemExit(f"missing closed theorem: {theorem}")

for boundary in [
    "existence of a partitioned budget certificate for arbitrary physical detector fields",
    "derivation of partitioned budget certificates from continuum GR data",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem"
]:
    if boundary not in data.get("does_not_prove", []):
        raise SystemExit(f"missing boundary: {boundary}")

for token in [
    "DERIVED_GATE_BOUND_FROM_PARTITIONED_BUDGET_CERTIFICATE",
    "removes that circularity",
    "two-detector example",
    "does not prove"
]:
    if token not in doc_text:
        raise SystemExit(f"missing doc token: {token}")

print("PARTITIONED_BUDGET_PHYSICAL_DETECTOR_GATE_BOUND_OK")
