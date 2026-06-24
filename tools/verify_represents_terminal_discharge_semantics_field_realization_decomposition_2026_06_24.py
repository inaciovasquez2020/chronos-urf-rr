#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/external_validation/represents_terminal_discharge_semantics_field_realization_decomposition_2026_06_24.json"
DOC = ROOT / "docs/status/REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_DECOMPOSITION_2026_06_24.md"

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["target"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_DECOMPOSITION"
    assert data["status"] == "partial_decomposition_recorded_not_realized"

    realized = data["realized_component"]
    assert realized["field"] == "r1LongChordExclusion"
    assert realized["object"] == "r1_concrete_newstein_fgl_source_long_chord_discharge_target"
    assert realized["status"] == "realized_for_R1ConcreteNativeSafeSemanticData"

    unrealized_fields = {item["field"] for item in data["unrealized_components"]}
    assert unrealized_fields == {
        "r1DiameterSeparationFillingObstruction",
        "r1UniformLocalTypeCapacity",
        "r1SourceToNativeCompatibility",
    }

    for token in [
        "R1ConcreteNewsteinFGLToNativeMapInputContract",
        "r1LongChordExclusion",
        "r1DiameterSeparationFillingObstruction",
        "r1UniformLocalTypeCapacity",
        "r1SourceToNativeCompatibility",
        "NO_DISCHARGED_R1_DIAMETER_SEPARATION_FILLING_OBSTRUCTION_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT",
        "NO_DISCHARGED_R1_UNIFORM_LOCAL_TYPE_CAPACITY_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT",
        "NO_DISCHARGED_R1_SOURCE_TO_NATIVE_COMPATIBILITY_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT",
    ]:
        assert token in doc

    for token in [
        "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_proved",
        "BOUNDARY := not R1DiameterSeparationFillingObstructionDischargeTarget_evidence_supplied",
        "BOUNDARY := not R1UniformLocalTypeCapacityDischargeTarget_evidence_supplied",
        "BOUNDARY := not R1SourceToNativeCompatibilityDischargeTarget_evidence_supplied",
        "BOUNDARY := not DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally",
        "BOUNDARY := not unrestricted_terminal_closure_proved_nonconditionally",
        "BOUNDARY := not final_closure_claim_proved",
    ]:
        assert token in data["boundaries"]
        assert token in doc

    print("REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_DECOMPOSITION_2026_06_24_OK")

if __name__ == "__main__":
    main()
