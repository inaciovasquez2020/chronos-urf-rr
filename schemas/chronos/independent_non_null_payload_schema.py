from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Any, Literal, Sequence, Union
import json
import math
import re

SCHEMA_VERSION = "2026-06-01.v1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class MassUnit(str, Enum):
    MM_EWH = "mm_EWH"
    KG_M2 = "kg_m2"
    MICROGAL = "microGal"


class CoordinateSystem(str, Enum):
    WGS84_GEOGRAPHIC = "WGS84_geographic"
    MASCON_ID = "MASCON_ID"


@dataclass(frozen=True)
class SpatialCoordinate:
    latitude_deg: float
    longitude_deg: float
    depth_m: float = 0.0

    def validate(self) -> None:
        _require_finite(self.latitude_deg, "latitude_deg")
        _require_finite(self.longitude_deg, "longitude_deg")
        _require_finite(self.depth_m, "depth_m")
        if not -90.0 <= self.latitude_deg <= 90.0:
            raise ValueError(f"latitude_deg out of range: {self.latitude_deg}")
        if not -180.0 <= self.longitude_deg <= 180.0:
            raise ValueError(f"longitude_deg out of range: {self.longitude_deg}")


@dataclass(frozen=True)
class MasconRow:
    mascon_id: int
    latitude_deg: float
    longitude_deg: float
    value: float
    unit: MassUnit

    def validate(self, expected_unit: MassUnit) -> None:
        if not isinstance(self.mascon_id, int) or self.mascon_id <= 0:
            raise ValueError("mascon_id must be a positive integer")
        SpatialCoordinate(self.latitude_deg, self.longitude_deg).validate()
        _require_finite(self.value, "row.value")
        if self.unit != expected_unit:
            raise ValueError(f"row unit {self.unit!r} does not match payload unit {expected_unit!r}")


@dataclass(frozen=True)
class PredictiveModelMetadata:
    model_name: str
    model_version: str
    generation_timestamp: str
    independence_certificate_sha256: str
    independent_of_lwe_baseline: Literal[True] = True

    def validate(self) -> None:
        _require_nonempty(self.model_name, "model_name")
        _require_nonempty(self.model_version, "model_version")
        _require_iso8601(self.generation_timestamp, "generation_timestamp")
        _require_sha256(self.independence_certificate_sha256, "independence_certificate_sha256")
        if self.independent_of_lwe_baseline is not True:
            raise ValueError("independent_of_lwe_baseline must be True")


@dataclass(frozen=True)
class IndependentNonNullPredictiveModelVector:
    metadata: PredictiveModelMetadata
    coordinates: Sequence[SpatialCoordinate]
    values: Sequence[float]
    unit: MassUnit
    route: Literal["A"] = field(default="A", init=False)
    schema_version: str = field(default=SCHEMA_VERSION, init=False)

    def validate(self) -> None:
        self.metadata.validate()
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"schema_version must be {SCHEMA_VERSION}")
        if len(self.coordinates) == 0:
            raise ValueError("coordinates must be non-empty")
        if len(self.values) == 0:
            raise ValueError("values must be non-empty")
        if len(self.values) != len(self.coordinates):
            raise ValueError(f"values length {len(self.values)} != coordinates length {len(self.coordinates)}")
        for i, coord in enumerate(self.coordinates):
            coord.validate()
            _require_finite(self.values[i], f"values[{i}]")
        if not any(v != 0.0 for v in self.values):
            raise ValueError("Route A vector must be non-null: at least one value must be nonzero")


@dataclass(frozen=True)
class GravityPayloadProvenance:
    source_agency: str
    dataset_name: str
    dataset_version: str
    doi_or_url: str
    authenticated_by: str
    authentication_timestamp: str

    def validate(self) -> None:
        for key in ("source_agency", "dataset_name", "dataset_version", "doi_or_url", "authenticated_by"):
            _require_nonempty(getattr(self, key), key)
        _require_iso8601(self.authentication_timestamp, "authentication_timestamp")


@dataclass(frozen=True)
class ReproducibleRunResult:
    run_id: str
    pipeline_version: str
    execution_timestamp: str
    input_hash_sha256: str
    output_hash_sha256: str
    command_or_notebook: str

    def validate(self) -> None:
        for key in ("run_id", "pipeline_version", "command_or_notebook"):
            _require_nonempty(getattr(self, key), key)
        _require_iso8601(self.execution_timestamp, "execution_timestamp")
        _require_sha256(self.input_hash_sha256, "input_hash_sha256")
        _require_sha256(self.output_hash_sha256, "output_hash_sha256")


@dataclass(frozen=True)
class ComparisonMetric:
    metric_name: str
    reference_label: str
    value: float
    unit: str

    def validate(self) -> None:
        _require_nonempty(self.metric_name, "metric_name")
        _require_nonempty(self.reference_label, "reference_label")
        _require_finite(self.value, "metric.value")
        _require_nonempty(self.unit, "metric.unit")


@dataclass(frozen=True)
class ExternalGravityPayloadResult:
    provenance: GravityPayloadProvenance
    coordinate_system: CoordinateSystem
    unit: MassUnit
    rows: Sequence[MasconRow]
    comparison_metrics: Sequence[ComparisonMetric]
    run_result: ReproducibleRunResult
    route: Literal["B"] = field(default="B", init=False)
    schema_version: str = field(default=SCHEMA_VERSION, init=False)

    def validate(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"schema_version must be {SCHEMA_VERSION}")
        self.provenance.validate()
        self.run_result.validate()
        if len(self.rows) == 0:
            raise ValueError("rows must be non-empty")
        if len(self.comparison_metrics) == 0:
            raise ValueError("comparison_metrics must be non-empty")
        for row in self.rows:
            row.validate(self.unit)
        for metric in self.comparison_metrics:
            metric.validate()


IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult = Union[
    IndependentNonNullPredictiveModelVector,
    ExternalGravityPayloadResult,
]


def validate_payload(payload: IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult) -> None:
    if isinstance(payload, (IndependentNonNullPredictiveModelVector, ExternalGravityPayloadResult)):
        payload.validate()
        return
    raise TypeError(f"unknown payload type: {type(payload).__name__}")


def required_input_supplied(payload: IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult) -> bool:
    validate_payload(payload)
    return True


def canonical_json(payload: IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult) -> str:
    validate_payload(payload)
    return json.dumps(_to_jsonable(payload), sort_keys=True, separators=(",", ":"))


def canonical_sha256(payload: IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult) -> str:
    return sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def payload_to_dict(payload: IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult) -> dict[str, Any]:
    validate_payload(payload)
    return _to_jsonable(payload)


def payload_from_dict(data: dict[str, Any]) -> IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult:
    route = data.get("route")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {SCHEMA_VERSION}")

    if route == "A":
        payload = IndependentNonNullPredictiveModelVector(
            metadata=PredictiveModelMetadata(**data["metadata"]),
            coordinates=[SpatialCoordinate(**c) for c in data["coordinates"]],
            values=list(data["values"]),
            unit=MassUnit(data["unit"]),
        )
    elif route == "B":
        payload = ExternalGravityPayloadResult(
            provenance=GravityPayloadProvenance(**data["provenance"]),
            coordinate_system=CoordinateSystem(data["coordinate_system"]),
            unit=MassUnit(data["unit"]),
            rows=[MasconRow(mascon_id=r["mascon_id"], latitude_deg=r["latitude_deg"], longitude_deg=r["longitude_deg"], value=r["value"], unit=MassUnit(r["unit"])) for r in data["rows"]],
            comparison_metrics=[ComparisonMetric(**m) for m in data["comparison_metrics"]],
            run_result=ReproducibleRunResult(**data["run_result"]),
        )
    else:
        raise ValueError(f"unknown route: {route!r}")

    validate_payload(payload)
    return payload


def make_route_a_stub() -> IndependentNonNullPredictiveModelVector:
    now = _now_iso()
    empty_sha = sha256(b"independence-certificate-stub").hexdigest()
    return IndependentNonNullPredictiveModelVector(
        metadata=PredictiveModelMetadata(
            model_name="DFM-MKC",
            model_version="0.0.1",
            generation_timestamp=now,
            independence_certificate_sha256=empty_sha,
            independent_of_lwe_baseline=True,
        ),
        coordinates=[SpatialCoordinate(latitude_deg=-15.0, longitude_deg=-47.0)],
        values=[1.0],
        unit=MassUnit.MM_EWH,
    )


def make_route_b_stub() -> ExternalGravityPayloadResult:
    now = _now_iso()
    empty_sha = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    return ExternalGravityPayloadResult(
        provenance=GravityPayloadProvenance(
            source_agency="NASA JPL",
            dataset_name="GRACE-FO RL06 MASCON",
            dataset_version="v02",
            doi_or_url="https://doi.org/10.5067/TEMSC-3JC62",
            authenticated_by="pipeline@example.org",
            authentication_timestamp=now,
        ),
        coordinate_system=CoordinateSystem.MASCON_ID,
        unit=MassUnit.MM_EWH,
        rows=[MasconRow(mascon_id=1, latitude_deg=-15.0, longitude_deg=-47.0, value=-12.3, unit=MassUnit.MM_EWH)],
        comparison_metrics=[ComparisonMetric(metric_name="RMSE", reference_label="observed_LWE_baseline", value=8.4, unit="mm_EWH")],
        run_result=ReproducibleRunResult(
            run_id="run-001",
            pipeline_version="1.0.0",
            execution_timestamp=now,
            input_hash_sha256=empty_sha,
            output_hash_sha256=empty_sha,
            command_or_notebook="python run_pipeline.py --config config.yaml",
        ),
    )


def _require_nonempty(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")


def _require_finite(value: float, name: str) -> None:
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _require_sha256(value: str, name: str) -> None:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise ValueError(f"{name} must be a lowercase SHA-256 hex digest")


def _require_iso8601(value: str, name: str) -> None:
    _require_nonempty(value, name)
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{name} must be ISO-8601") from exc


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _to_jsonable(obj: Any) -> Any:
    if isinstance(obj, Enum):
        return obj.value
    if is_dataclass(obj):
        return {k: _to_jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    return obj


if __name__ == "__main__":
    a = make_route_a_stub()
    b = make_route_b_stub()
    validate_payload(a)
    validate_payload(b)
    assert required_input_supplied(a) is True
    assert required_input_supplied(b) is True
    assert payload_from_dict(payload_to_dict(a)) == a
    assert payload_from_dict(payload_to_dict(b)) == b
    print("INDEPENDENT_NON_NULL_PAYLOAD_SCHEMA_SMOKE_OK")
    print(json.dumps({
        "route_a_sha256": canonical_sha256(a),
        "route_b_sha256": canonical_sha256(b),
        "schema_version": SCHEMA_VERSION,
    }, indent=2, sort_keys=True))
