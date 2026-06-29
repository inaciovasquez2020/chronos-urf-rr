#!/usr/bin/env python3
import json
from pathlib import Path

path = Path("artifacts/external_validation/finite_jet_rigidity_operator_boundary_2026_06_28.json")
data = json.loads(path.read_text())

required_top = {
    "artifact",
    "date",
    "status",
    "operator",
    "diagnostics",
    "dimension_contract",
    "verifier_scope",
    "boundaries",
}
missing_top = required_top - set(data)
if missing_top:
    raise SystemExit(f"MISSING_FIELD := {sorted(missing_top)}")

if data["status"] != "boundary_only":
    raise SystemExit("INVALID_STATUS := expected boundary_only")

operator = data["operator"]
for key in [
    "name",
    "symbol",
    "jet_order",
    "ambient_dimension",
    "nodes",
    "edges",
    "projection_axis_tokens",
]:
    if key not in operator:
        raise SystemExit(f"MISSING_OPERATOR_FIELD := {key}")

for key in [
    "jet_order",
    "ambient_dimension",
    "nodes",
    "edges",
    "projection_axis_tokens",
]:
    if operator[key].get("claim") != "input_only":
        raise SystemExit(f"INVALID_OPERATOR_CLAIM := {key}")

diagnostics = data["diagnostics"]
if diagnostics.get("rank_deficiency_calculator") != "diagnostic_only":
    raise SystemExit("INVALID_DIAGNOSTIC_SCOPE := rank_deficiency_calculator")
if diagnostics.get("eigenvalue_decay") != "not_mapped_to_overlap_axis":
    raise SystemExit("INVALID_DIAGNOSTIC_SCOPE := eigenvalue_decay")
if diagnostics.get("overlap_axis_mapping") is not False:
    raise SystemExit("INVALID_OVERLAP_AXIS_MAPPING_FLAG")

dimension_contract = data["dimension_contract"]
for key in [
    "checks_positive_jet_order",
    "checks_positive_ambient_dimension",
    "checks_nonempty_nodes",
    "checks_edge_count_token",
    "checks_projection_axis_token_count",
]:
    if dimension_contract.get(key) is not True:
        raise SystemExit(f"INVALID_DIMENSION_CONTRACT := {key}")

scope = data["verifier_scope"]
required_true = [
    "checks_schema",
    "checks_dimension_tokens",
    "checks_nonclaim_flags",
]
for key in required_true:
    if scope.get(key) is not True:
        raise SystemExit(f"INVALID_VERIFIER_SCOPE := {key}")

required_false = [
    "computes_rank",
    "computes_eigenvalue_decay",
    "maps_eigenvalue_decay_to_overlap_axis",
    "computes_einstein_tensor",
    "computes_metric_backreaction",
    "claims_gravity_closure",
]
for key in required_false:
    if scope.get(key) is not False:
        raise SystemExit(f"INVALID_NONCLAIM_FLAG := {key}")

required_boundaries = {
    "not_einstein_limit",
    "no_gravity_closure",
    "no_physical_metric_backreaction",
    "no_continuous_spacetime_curvature_claim",
    "rank_deficiency_diagnostic_only",
    "no_overlap_axis_eigenvalue_decay_mapping",
}
if not required_boundaries.issubset(set(data["boundaries"])):
    raise SystemExit("MISSING_BOUNDARY_TOKEN")

print("FINITE_JET_RIGIDITY_OPERATOR_BOUNDARY_OK")
