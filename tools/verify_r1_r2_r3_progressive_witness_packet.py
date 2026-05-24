#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "artifacts/chronos/r1_r2_r3_progressive_witness_packet_2026_05_24.json"
COND_ART = ROOT / "artifacts/chronos/r1_r2_r3_isolated_targets_conditional_closure_2026_05_24.json"
COND_LEAN = ROOT / "lean/Chronos/Frontier/R1R2R3IsolatedTargetsConditionalClosure.lean"
DOC = ROOT / "docs/status/R1_R2_R3_PROGRESSIVE_WITNESS_PACKET_2026_05_24.md"

TARGET_KEYS = ["R1", "R2", "R3", "CLOSURE"]
ALLOWED_STATES = {"PENDING", "SUPPLIED", "VERIFIED"}
BOUNDARY = [
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
EXPECTED_NAMES = {
    "R1": "LongChordExclusionProofTarget",
    "R2": "DiameterSeparationFillingObstructionProofTarget",
    "R3": "UniformLocalTypeCapacityProofTarget",
    "CLOSURE": "RepositoryNativeR1R2R3BindingClosureConditionalTarget",
}

def fail(msg: str) -> None:
    raise SystemExit(f"R1_R2_R3_PROGRESSIVE_WITNESS_PACKET_FAILED: {msg}")

def require(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)

def rooted_exists(path_value) -> bool:
    if not path_value or not isinstance(path_value, str):
        return False
    return (ROOT / path_value).exists()

def check_base(packet: dict) -> None:
    require(packet.get("artifact") == "R1_R2_R3_PROGRESSIVE_WITNESS_PACKET", "wrong artifact")
    require(packet.get("status") == "PROGRESSIVE_TEST_HARNESS_ONLY_FRONTIER_OPEN", "wrong status")
    require(packet.get("linked_conditional_surface") == "R1_R2_R3_ISOLATED_TARGETS_CONDITIONAL_CLOSURE", "wrong linked surface")
    require(isinstance(packet.get("piece_by_piece_order"), list), "missing staged order")
    require(len(packet["piece_by_piece_order"]) == 11, "staged order must have 11 pieces")

    require(COND_ART.exists(), "missing linked conditional artifact")
    require(COND_LEAN.exists(), "missing linked conditional Lean module")
    require(DOC.exists(), "missing progressive witness status doc")

    targets = packet.get("targets")
    require(isinstance(targets, dict), "targets must be object")
    require(sorted(targets.keys()) == sorted(TARGET_KEYS), "targets must be exactly R1/R2/R3/CLOSURE")

    for key in TARGET_KEYS:
        target = targets[key]
        require(target.get("name") == EXPECTED_NAMES[key], f"{key} has wrong target name")
        require(target.get("state") in ALLOWED_STATES, f"{key} has invalid state")
        require("mathematical_statement" in target, f"{key} missing mathematical_statement")
        require("data_packet_path" in target, f"{key} missing data_packet_path")
        require("checker_path" in target, f"{key} missing checker_path")
        require("lean_artifact_path" in target, f"{key} missing lean_artifact_path")
        require("proof_artifact_path" in target, f"{key} missing proof_artifact_path")
        require("verification_result" in target, f"{key} missing verification_result")

    for token in BOUNDARY:
        require(token in packet.get("does_not_prove", []), f"missing packet boundary: {token}")
        require(token in DOC.read_text(), f"missing doc boundary: {token}")

def check_strict(packet: dict) -> None:
    require(packet.get("closure_ready") is True, "strict mode requires closure_ready true")
    require(packet.get("strict_completion_status") == "READY", "strict mode requires READY status")

    for key in TARGET_KEYS:
        target = packet["targets"][key]
        require(target.get("state") == "VERIFIED", f"{key} must be VERIFIED")
        require(isinstance(target.get("mathematical_statement"), str) and target["mathematical_statement"].strip(),
                f"{key} needs nonempty mathematical_statement")
        require(rooted_exists(target.get("lean_artifact_path")), f"{key} lean_artifact_path must exist")
        require(rooted_exists(target.get("proof_artifact_path")), f"{key} proof_artifact_path must exist")
        require(target.get("verification_result") == "VERIFIED_BY_REPOSITORY_NATIVE_PROOF",
                f"{key} must be verified by repository-native proof")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", nargs="?", default=str(DEFAULT_PACKET))
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    packet_path = Path(args.packet)
    if not packet_path.is_absolute():
        packet_path = ROOT / packet_path

    try:
        packet = json.loads(packet_path.read_text())
    except Exception as exc:
        fail(f"could not read packet: {exc}")

    check_base(packet)

    if packet.get("closure_ready") is True or packet.get("strict_completion_status") == "READY":
        check_strict(packet)

    if args.strict:
        check_strict(packet)
        print("R1_R2_R3_PROGRESSIVE_WITNESS_PACKET_STRICT_OK")
    else:
        print("R1_R2_R3_PROGRESSIVE_WITNESS_PACKET_OPEN_FRONTIER_OK")

if __name__ == "__main__":
    main()
