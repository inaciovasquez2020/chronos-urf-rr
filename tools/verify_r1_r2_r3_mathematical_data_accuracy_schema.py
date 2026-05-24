#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "artifacts/chronos/r1_r2_r3_mathematical_data_accuracy_schema_2026_05_24.json"
PACKET = ROOT / "artifacts/chronos/r1_r2_r3_progressive_witness_packet_2026_05_24.json"
DOC = ROOT / "docs/status/R1_R2_R3_MATHEMATICAL_DATA_ACCURACY_SCHEMA_2026_05_24.md"

TARGETS = [
    "R1_LONG_CHORD_EXCLUSION",
    "R2_DIAMETER_SEPARATION_FILLING_OBSTRUCTION",
    "R3_UNIFORM_LOCAL_TYPE_CAPACITY",
]

REQUIRED_FIELDS = [
    "formal_statement",
    "domain",
    "objects",
    "invariants",
    "obstruction_or_capacity_quantity",
    "finite_witness_schema",
    "proof_dependencies",
    "checker_contract",
    "lean_target",
    "boundary",
]

BOUNDARY = [
    "mathematical accuracy",
    "truth accuracy",
    "native R1/R2/R3 instance",
    "LongChordExclusion",
    "DiameterSeparationFillingObstruction",
    "UniformLocalTypeCapacity",
    "NON_FACTORISATION",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

def fail(msg: str) -> None:
    raise SystemExit(f"R1_R2_R3_MATHEMATICAL_DATA_ACCURACY_SCHEMA_FAILED: {msg}")

def require(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)

def structural_score(data: dict) -> tuple[int, int]:
    total = 0
    filled = 0
    for key in TARGETS:
        target = data["targets"][key]
        for field in REQUIRED_FIELDS:
            total += 1
            value = target[field]
            if value not in (None, [], {}, ""):
                filled += 1
    return filled, total

def main() -> None:
    require(SCHEMA.exists(), "missing schema artifact")
    require(PACKET.exists(), "missing linked progressive packet")
    require(DOC.exists(), "missing status doc")

    data = json.loads(SCHEMA.read_text())
    require(data["artifact"] == "R1_R2_R3_MATHEMATICAL_DATA_ACCURACY_SCHEMA", "wrong artifact")
    require(data["status"] == "MATHEMATICAL_DATA_SCHEMA_ONLY_NO_ACCURACY_CLAIM", "wrong status")
    require(data["linked_progressive_packet"] == "artifacts/chronos/r1_r2_r3_progressive_witness_packet_2026_05_24.json", "wrong linked packet")

    policy = data["accuracy_policy"]
    require(policy["score_type"] == "STRUCTURAL_COMPLETENESS_ONLY", "wrong score type")
    require(policy["truth_accuracy_claim"] is False, "truth accuracy must be false")
    require(policy["empirical_accuracy_claim"] is False, "empirical accuracy must be false")
    require(policy["theorem_accuracy_claim"] is False, "theorem accuracy must be false")
    require(policy["minimum_verified_fields_per_target"] == REQUIRED_FIELDS, "wrong minimum field list")

    require(sorted(data["targets"].keys()) == sorted(TARGETS), "wrong target set")
    for key in TARGETS:
        target = data["targets"][key]
        for field in REQUIRED_FIELDS:
            require(field in target, f"{key} missing {field}")
        require(isinstance(target["objects"], list), f"{key}.objects must be list")
        require(isinstance(target["invariants"], list), f"{key}.invariants must be list")
        require(isinstance(target["proof_dependencies"], list), f"{key}.proof_dependencies must be list")
        require(isinstance(target["finite_witness_schema"], dict), f"{key}.finite_witness_schema must be object")

    for token in BOUNDARY:
        require(token in data["does_not_prove"], f"missing artifact boundary: {token}")
        require(token in DOC.read_text(), f"missing doc boundary: {token}")

    filled, total = structural_score(data)
    print(f"R1_R2_R3_MATHEMATICAL_DATA_ACCURACY_SCHEMA_OK structural_completeness={filled}/{total}")

if __name__ == "__main__":
    main()
