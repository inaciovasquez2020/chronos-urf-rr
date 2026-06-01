#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO / "schemas/chronos/independent_non_null_payload_schema.py"
DEFAULT_OUT = REPO / "artifacts/chronos/independent_non_null_payload_result_ingested_latest.json"


def load_schema():
    spec = importlib.util.spec_from_file_location("independent_non_null_payload_schema", SCHEMA_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and normalize an IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult payload."
    )
    parser.add_argument("payload_json", help="Filled Route A or Route B JSON payload")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output artifact path")
    args = parser.parse_args()

    schema = load_schema()
    payload_path = Path(args.payload_json)
    out = Path(args.out)

    data = json.loads(payload_path.read_text())
    payload = schema.payload_from_dict(data)
    schema.validate_payload(payload)

    normalized = schema.payload_to_dict(payload)
    result = {
        "object": "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT",
        "status": "PAYLOAD_RESULT_SUPPLIED_AND_SCHEMA_VALIDATED",
        "decision": "PASS",
        "schema_version": normalized["schema_version"],
        "route": normalized["route"],
        "source_payload": str(payload_path),
        "canonical_sha256": schema.canonical_sha256(payload),
        "required_input_supplied": schema.required_input_supplied(payload),
        "normalized_payload": normalized,
        "next_admissible_object": "INDEPENDENT_NON_NULL_PAYLOAD_RESULT_COMPARISON_OR_INTERPRETATION",
        "weakest_sufficient_next_input": "IndependentNonNullPayloadResultComparisonOrInterpretation"
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print("INDEPENDENT_NON_NULL_PAYLOAD_RESULT_INGESTED")
    print(json.dumps({
        "artifact": str(out),
        "decision": result["decision"],
        "route": result["route"],
        "required_input_supplied": result["required_input_supplied"],
        "canonical_sha256": result["canonical_sha256"],
        "next_admissible_object": result["next_admissible_object"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
