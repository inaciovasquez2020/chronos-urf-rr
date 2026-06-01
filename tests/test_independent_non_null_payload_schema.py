import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ART = Path("artifacts/chronos/independent_non_null_payload_schema_2026_06_01.json")
PY_SCHEMA = Path("schemas/chronos/independent_non_null_payload_schema.py")
TS_SCHEMA = Path("schemas/chronos/independent_non_null_payload_schema.ts")
VERIFY = Path("tools/verify_independent_non_null_payload_schema.py")


def load_schema():
    spec = importlib.util.spec_from_file_location("independent_non_null_payload_schema", PY_SCHEMA)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_schema_artifact_status():
    data = json.loads(ART.read_text())
    assert data["status"] == "SCHEMA_CLOSED_PAYLOAD_RESULT_NOT_SUPPLIED"
    assert data["required_input_supplied"] is False
    assert data["schema_version"] == "2026-06-01.v1"


def test_route_a_and_b_stubs_validate():
    mod = load_schema()
    a = mod.make_route_a_stub()
    b = mod.make_route_b_stub()
    mod.validate_payload(a)
    mod.validate_payload(b)
    assert mod.required_input_supplied(a) is True
    assert mod.required_input_supplied(b) is True


def test_route_a_rejects_all_zero_vector():
    mod = load_schema()
    a = mod.make_route_a_stub()
    bad = mod.IndependentNonNullPredictiveModelVector(
        metadata=a.metadata,
        coordinates=a.coordinates,
        values=[0.0 for _ in a.values],
        unit=a.unit,
    )
    try:
        mod.validate_payload(bad)
    except ValueError as exc:
        assert "nonzero" in str(exc)
    else:
        raise AssertionError("all-zero vector validated")


def test_route_b_rejects_unit_mismatch():
    mod = load_schema()
    b = mod.make_route_b_stub()
    bad_rows = [
        mod.MasconRow(
            mascon_id=b.rows[0].mascon_id,
            latitude_deg=b.rows[0].latitude_deg,
            longitude_deg=b.rows[0].longitude_deg,
            value=b.rows[0].value,
            unit=mod.MassUnit.KG_M2,
        )
    ]
    bad = mod.ExternalGravityPayloadResult(
        provenance=b.provenance,
        coordinate_system=b.coordinate_system,
        unit=mod.MassUnit.MM_EWH,
        rows=bad_rows,
        comparison_metrics=b.comparison_metrics,
        run_result=b.run_result,
    )
    try:
        mod.validate_payload(bad)
    except ValueError as exc:
        assert "does not match" in str(exc)
    else:
        raise AssertionError("unit mismatch validated")


def test_payload_round_trip():
    mod = load_schema()
    a = mod.make_route_a_stub()
    b = mod.make_route_b_stub()
    assert mod.payload_from_dict(mod.payload_to_dict(a)) == a
    assert mod.payload_from_dict(mod.payload_to_dict(b)) == b


def test_typescript_schema_contains_runtime_guards():
    text = TS_SCHEMA.read_text()
    assert "Number.isFinite" in text
    assert "at least one value must be nonzero" in text
    assert "requiredInputSupplied" in text
    assert "independence_certificate_sha256" in text


def test_schema_verifier():
    result = subprocess.run(["python3", str(VERIFY)], text=True, capture_output=True, check=True)
    assert "INDEPENDENT_NON_NULL_PAYLOAD_SCHEMA_OK" in result.stdout
    assert '"decision": "PASS"' in result.stdout
