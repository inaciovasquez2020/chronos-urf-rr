export const SCHEMA_VERSION = "2026-06-01.v1" as const;

export type MassUnit = "mm_EWH" | "kg_m2" | "microGal";
export type CoordinateSystem = "WGS84_geographic" | "MASCON_ID";
export type Sha256Hex = string;
export type Iso8601Timestamp = string;
export type NonEmptyArray<T> = [T, ...T[]];

export interface SpatialCoordinate {
  latitude_deg: number;
  longitude_deg: number;
  depth_m?: number;
}

export interface MasconRow {
  mascon_id: number;
  latitude_deg: number;
  longitude_deg: number;
  value: number;
  unit: MassUnit;
}

export interface PredictiveModelMetadata {
  model_name: string;
  model_version: string;
  generation_timestamp: Iso8601Timestamp;
  independence_certificate_sha256: Sha256Hex;
  independent_of_lwe_baseline: true;
}

export interface IndependentNonNullPredictiveModelVector {
  schema_version: typeof SCHEMA_VERSION;
  route: "A";
  metadata: PredictiveModelMetadata;
  coordinates: NonEmptyArray<SpatialCoordinate>;
  values: NonEmptyArray<number>;
  unit: MassUnit;
}

export interface GravityPayloadProvenance {
  source_agency: string;
  dataset_name: string;
  dataset_version: string;
  doi_or_url: string;
  authenticated_by: string;
  authentication_timestamp: Iso8601Timestamp;
}

export interface ReproducibleRunResult {
  run_id: string;
  pipeline_version: string;
  execution_timestamp: Iso8601Timestamp;
  input_hash_sha256: Sha256Hex;
  output_hash_sha256: Sha256Hex;
  command_or_notebook: string;
}

export interface ComparisonMetric {
  metric_name: string;
  reference_label: string;
  value: number;
  unit: string;
}

export interface ExternalGravityPayloadResult {
  schema_version: typeof SCHEMA_VERSION;
  route: "B";
  provenance: GravityPayloadProvenance;
  coordinate_system: CoordinateSystem;
  unit: MassUnit;
  rows: NonEmptyArray<MasconRow>;
  comparison_metrics: NonEmptyArray<ComparisonMetric>;
  run_result: ReproducibleRunResult;
}

export type IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult =
  | IndependentNonNullPredictiveModelVector
  | ExternalGravityPayloadResult;

const SHA256_RE = /^[0-9a-f]{64}$/;

function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null;
}

function isFiniteNumber(v: unknown): v is number {
  return typeof v === "number" && Number.isFinite(v);
}

function assertNonEmptyString(v: unknown, name: string): asserts v is string {
  if (typeof v !== "string" || v.trim().length === 0) {
    throw new Error(`${name} must be a non-empty string`);
  }
}

function assertSha256(v: unknown, name: string): asserts v is string {
  if (typeof v !== "string" || !SHA256_RE.test(v)) {
    throw new Error(`${name} must be a lowercase SHA-256 hex digest`);
  }
}

function assertIso8601(v: unknown, name: string): asserts v is string {
  assertNonEmptyString(v, name);
  if (Number.isNaN(Date.parse(v))) {
    throw new Error(`${name} must be ISO-8601`);
  }
}

function assertCoordinate(c: SpatialCoordinate, name: string): void {
  if (!isFiniteNumber(c.latitude_deg) || c.latitude_deg < -90 || c.latitude_deg > 90) {
    throw new Error(`${name}.latitude_deg out of range`);
  }
  if (!isFiniteNumber(c.longitude_deg) || c.longitude_deg < -180 || c.longitude_deg > 180) {
    throw new Error(`${name}.longitude_deg out of range`);
  }
  if (c.depth_m !== undefined && !isFiniteNumber(c.depth_m)) {
    throw new Error(`${name}.depth_m must be finite`);
  }
}

function validateRouteA(p: IndependentNonNullPredictiveModelVector): void {
  if (p.schema_version !== SCHEMA_VERSION) throw new Error(`schema_version must be ${SCHEMA_VERSION}`);
  assertNonEmptyString(p.metadata.model_name, "metadata.model_name");
  assertNonEmptyString(p.metadata.model_version, "metadata.model_version");
  assertIso8601(p.metadata.generation_timestamp, "metadata.generation_timestamp");
  assertSha256(p.metadata.independence_certificate_sha256, "metadata.independence_certificate_sha256");
  if (p.metadata.independent_of_lwe_baseline !== true) {
    throw new Error("Route A: metadata.independent_of_lwe_baseline must be true");
  }
  if (p.coordinates.length === 0) throw new Error("Route A: coordinates must be non-empty");
  if (p.values.length === 0) throw new Error("Route A: values must be non-empty");
  if (p.values.length !== p.coordinates.length) {
    throw new Error(`Route A: values.length (${p.values.length}) !== coordinates.length (${p.coordinates.length})`);
  }
  p.coordinates.forEach((c, i) => assertCoordinate(c, `coordinates[${i}]`));
  p.values.forEach((v, i) => {
    if (!isFiniteNumber(v)) throw new Error(`Route A: values[${i}] must be finite`);
  });
  if (!p.values.some((v) => v !== 0)) {
    throw new Error("Route A vector must be non-null: at least one value must be nonzero");
  }
}

function validateRouteB(p: ExternalGravityPayloadResult): void {
  if (p.schema_version !== SCHEMA_VERSION) throw new Error(`schema_version must be ${SCHEMA_VERSION}`);
  const prov = p.provenance;
  assertNonEmptyString(prov.source_agency, "provenance.source_agency");
  assertNonEmptyString(prov.dataset_name, "provenance.dataset_name");
  assertNonEmptyString(prov.dataset_version, "provenance.dataset_version");
  assertNonEmptyString(prov.doi_or_url, "provenance.doi_or_url");
  assertNonEmptyString(prov.authenticated_by, "provenance.authenticated_by");
  assertIso8601(prov.authentication_timestamp, "provenance.authentication_timestamp");

  if (p.rows.length === 0) throw new Error("Route B: rows must be non-empty");
  p.rows.forEach((r, i) => {
    if (!Number.isInteger(r.mascon_id) || r.mascon_id <= 0) throw new Error(`rows[${i}].mascon_id must be positive integer`);
    assertCoordinate(r, `rows[${i}]`);
    if (!isFiniteNumber(r.value)) throw new Error(`rows[${i}].value must be finite`);
    if (r.unit !== p.unit) throw new Error(`rows[${i}].unit must equal payload unit`);
  });

  if (p.comparison_metrics.length === 0) throw new Error("Route B: comparison_metrics must be non-empty");
  p.comparison_metrics.forEach((m, i) => {
    assertNonEmptyString(m.metric_name, `comparison_metrics[${i}].metric_name`);
    assertNonEmptyString(m.reference_label, `comparison_metrics[${i}].reference_label`);
    if (!isFiniteNumber(m.value)) throw new Error(`comparison_metrics[${i}].value must be finite`);
    assertNonEmptyString(m.unit, `comparison_metrics[${i}].unit`);
  });

  const run = p.run_result;
  assertNonEmptyString(run.run_id, "run_result.run_id");
  assertNonEmptyString(run.pipeline_version, "run_result.pipeline_version");
  assertIso8601(run.execution_timestamp, "run_result.execution_timestamp");
  assertSha256(run.input_hash_sha256, "run_result.input_hash_sha256");
  assertSha256(run.output_hash_sha256, "run_result.output_hash_sha256");
  assertNonEmptyString(run.command_or_notebook, "run_result.command_or_notebook");
}

export function validatePayload(payload: IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult): void {
  if (!isRecord(payload)) throw new TypeError("payload must be an object");
  if (payload.route === "A") validateRouteA(payload as IndependentNonNullPredictiveModelVector);
  else if (payload.route === "B") validateRouteB(payload as ExternalGravityPayloadResult);
  else throw new TypeError(`Unknown route: ${String(payload.route)}`);
}

export function requiredInputSupplied(payload: IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult): true {
  validatePayload(payload);
  return true;
}
