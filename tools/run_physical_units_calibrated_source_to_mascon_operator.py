#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import io
import json
import math
import textwrap
import zipfile
from collections import Counter

import numpy as np
from scipy.special import lpmv

DATE_TAG = "2026_05_30"

SOURCE_NAME = "XGM2019e_2159"
SOURCE_DOI = "10.5880/ICGEM.2019.007"
SOURCE_URL = "https://icgem.gfz-potsdam.de/getmodel/zip/eeb03971cf6e533e6eeb6b010336463286dcda0846684248d5530acf8e800055/XGM2019e_2159.zip"
SOURCE_PAGE = "https://icgem.gfz-potsdam.de/tom"

GFC = Path("external_data/xgm2019e/XGM2019e_2159.gfc")
BASELINE = Path("data/mascon_vectors/baseline_vector.npy")
DEFICIT = Path("data/mascon_vectors/deficit_vector.npy")
PRIOR = Path("artifacts/gravity/physical_units_calibrated_source_to_mascon_operator_or_third_public_holdout_2026_05_30.json")

OUT_PHYSICAL_VECTOR = Path(f"data/gravity_external_vectors/xgm2019e_2159_physical_radial_gravity_disturbance_mgal_mascon_shape_{DATE_TAG}.npy")
OUT_NORMALIZED_VECTOR = Path(f"data/gravity_external_vectors/xgm2019e_2159_physical_operator_normalized_alignment_vector_{DATE_TAG}.npy")
OUT_ART = Path(f"artifacts/gravity/physical_units_calibrated_source_to_mascon_operator_{DATE_TAG}.json")
OUT_DOC = Path(f"docs/status/PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_{DATE_TAG}.md")

MAX_DEGREE_SYNTHESIS = 24

DEFAULT_GM = 3986004.415e8
DEFAULT_A = 6378136.3
EVALUATION_RADIUS_M = 6378136.3
MGAL_PER_M_PER_S2 = 100000.0

def request_bytes(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "chronos-urf-rr-validation/1.0"})
    with urlopen(req, timeout=240) as r:
        return r.read()

def download_gfc() -> str:
    GFC.parent.mkdir(parents=True, exist_ok=True)
    data = request_bytes(SOURCE_URL)

    if data[:4] == b"PK\x03\x04":
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            names = [n for n in z.namelist() if n.lower().endswith(".gfc") and "xgm2019e_2159" in n.lower()]
            if not names:
                names = [n for n in z.namelist() if n.lower().endswith(".gfc")]
            if not names:
                raise SystemExit("XGM2019e_2159 zip contained no .gfc file")
            GFC.write_bytes(z.read(names[0]))
            return SOURCE_URL

    if b"end_of_head" in data[:500000] or b"gfc" in data[:500000]:
        GFC.write_bytes(data)
        return SOURCE_URL

    raise SystemExit("downloaded XGM2019e_2159 payload was not a zip or GFC file")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def fnum(x: str) -> float:
    return float(x.replace("D", "E").replace("d", "e"))

def parse_gfc(path: Path, max_degree: int):
    coeffs = {}
    header = {}
    token_counts = Counter()
    numeric_rows = 0

    raw = path.read_bytes()
    if raw[:1] == b"<" or b"<html" in raw[:2048].lower():
        raise SystemExit("downloaded XGM2019e_2159 file appears to be HTML, not GFC coefficients")

    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue

            parts = s.split()
            token_counts[parts[0]] += 1

            key = parts[0].lower()
            if len(parts) >= 2 and key not in {"gfc", "gfct", "trnd", "acos", "asin"}:
                if not parts[0].lstrip("+-").isdigit():
                    header[parts[0]] = " ".join(parts[1:])

            if key in {"gfc", "gfct"} and len(parts) >= 5:
                n = int(parts[1])
                m = int(parts[2])
                c = fnum(parts[3])
                ss = fnum(parts[4])
            elif len(parts) >= 4 and parts[0].isdigit() and parts[1].isdigit():
                n = int(parts[0])
                m = int(parts[1])
                c = fnum(parts[2])
                ss = fnum(parts[3])
            else:
                continue

            numeric_rows += 1

            if 2 <= n <= max_degree:
                coeffs[(n, m)] = (c, ss)

    if not coeffs:
        raise SystemExit("no usable XGM2019e_2159 coefficients parsed")

    gm = fnum(header.get("earth_gravity_constant", str(DEFAULT_GM)).split()[0])
    a = fnum(header.get("radius", str(DEFAULT_A)).split()[0])

    return header, coeffs, numeric_rows, dict(token_counts.most_common(20)), gm, a


def finite_mean_std_array(x):
    y = np.asarray(x, dtype=np.float64).ravel()
    if y.size == 0:
        raise SystemExit("cannot compute finite statistics for empty array")
    if not np.all(np.isfinite(y)):
        raise SystemExit("raw physical grid contains non-finite values")
    mean = float(y.mean(dtype=np.float64))
    d = y - mean
    std = float(math.sqrt(float(np.dot(d, d)) / y.size))
    if not math.isfinite(mean) or not math.isfinite(std) or std == 0.0:
        raise SystemExit(f"invalid raw physical grid statistics: mean={mean}, std={std}")
    return mean, std

def synthesize_radial_gravity_mgal(coeffs, lat_count: int, lon_count: int, max_degree: int, gm: float, a: float, r: float):
    lats = np.linspace(-89.5, 89.5, lat_count, dtype=np.float64)
    lons = np.linspace(0.5, 359.5, lon_count, dtype=np.float64)

    phi = np.deg2rad(lons)
    sin_lat = np.sin(np.deg2rad(lats))

    grid_mps2 = np.zeros((lat_count, lon_count), dtype=np.float64)

    used = 0
    scale0 = gm / (r * r)

    for n in range(2, max_degree + 1):
        radial_factor = (n + 1) * (a / r) ** n
        for m in range(0, n + 1):
            c, s = coeffs.get((n, m), (0.0, 0.0))
            if c == 0.0 and s == 0.0:
                continue
            pnm = lpmv(m, n, sin_lat)
            trig = c * np.cos(m * phi) + s * np.sin(m * phi)
            grid_mps2 += scale0 * radial_factor * np.outer(pnm, trig)
            used += 1

    grid_mps2 = np.nan_to_num(grid_mps2, nan=0.0, posinf=0.0, neginf=0.0)
    grid_mgal = (grid_mps2 * MGAL_PER_M_PER_S2).astype(np.float32)

    raw_mean, raw_std = finite_mean_std_array(grid_mgal)

    if used == 0 or raw_std == 0.0:
        raise SystemExit(f"physical source grid invalid: used={used}, mean={raw_mean}, std={raw_std}")

    return grid_mgal, used, raw_mean, raw_std

def finite_mean_std_memmap(path: Path, chunk: int = 1_000_000):
    x = np.ravel(np.load(path, mmap_mode="r"))
    n = x.size
    total = 0.0
    total_sq_centered = 0.0

    for start in range(0, n, chunk):
        stop = min(start + chunk, n)
        block = x[start:stop].astype(np.float64)
        if not np.all(np.isfinite(block)):
            raise SystemExit("physical vector contains non-finite values")
        total += float(block.sum())

    mean = total / n

    for start in range(0, n, chunk):
        stop = min(start + chunk, n)
        block = x[start:stop].astype(np.float64)
        d = block - mean
        total_sq_centered += float(np.dot(d, d))

    std = math.sqrt(total_sq_centered / n)
    if not math.isfinite(std) or std == 0.0:
        raise SystemExit(f"invalid physical vector std: {std}")
    return mean, std

def normalize_vector_file(src_path: Path, out_path: Path, chunk: int = 1_000_000):
    x = np.ravel(np.load(src_path, mmap_mode="r"))
    mean, std = finite_mean_std_memmap(src_path, chunk=chunk)

    out = np.lib.format.open_memmap(
        out_path,
        mode="w+",
        dtype=np.float32,
        shape=x.shape,
    )

    for start in range(0, x.size, chunk):
        stop = min(start + chunk, x.size)
        out[start:stop] = ((x[start:stop].astype(np.float64) - mean) / std).astype(np.float32)

    del out
    return mean, std

def pair_metrics(a_path: Path, b_path: Path, chunk: int = 1_000_000):
    a = np.load(a_path, mmap_mode="r")
    b = np.load(b_path, mmap_mode="r")

    if a.shape != b.shape:
        raise SystemExit(f"shape mismatch: {a.shape} != {b.shape}")

    av = np.ravel(a)
    bv = np.ravel(b)
    n = av.size

    abs_sum = 0.0
    sq_sum = 0.0

    for start in range(0, n, chunk):
        stop = min(start + chunk, n)
        d = av[start:stop].astype(np.float64) - bv[start:stop].astype(np.float64)
        abs_sum += float(np.abs(d).sum())
        sq_sum += float(np.square(d).sum())

    return {
        "mean_absolute_delta": abs_sum / n,
        "root_mean_square_delta": math.sqrt(sq_sum / n),
    }

def main() -> None:
    for required in (BASELINE, DEFICIT, PRIOR):
        if not required.exists():
            raise SystemExit(f"missing required file: {required}")

    source_url_used = download_gfc()

    baseline = np.load(BASELINE, mmap_mode="r")
    deficit = np.load(DEFICIT, mmap_mode="r")

    if baseline.shape != deficit.shape:
        raise SystemExit(f"baseline shape {baseline.shape} != deficit shape {deficit.shape}")

    if baseline.ndim == 3:
        time_count, lat_count, lon_count = baseline.shape
    elif baseline.ndim == 1 and baseline.size % (360 * 720) == 0:
        time_count = baseline.size // (360 * 720)
        lat_count = 360
        lon_count = 720
    else:
        raise SystemExit(f"unsupported MASCON baseline shape: {baseline.shape}")

    header, coeffs, numeric_rows, token_prefixes, gm, a = parse_gfc(GFC, MAX_DEGREE_SYNTHESIS)

    physical_grid_mgal, used_terms, raw_mean_mgal, raw_std_mgal = synthesize_radial_gravity_mgal(
        coeffs=coeffs,
        lat_count=lat_count,
        lon_count=lon_count,
        max_degree=MAX_DEGREE_SYNTHESIS,
        gm=gm,
        a=a,
        r=EVALUATION_RADIUS_M,
    )

    if baseline.ndim == 3:
        physical_vector = np.broadcast_to(physical_grid_mgal, baseline.shape).astype(np.float32)
    else:
        physical_vector = np.broadcast_to(
            physical_grid_mgal.reshape(-1),
            (time_count, lat_count * lon_count),
        ).reshape(-1).astype(np.float32)

    Path(OUT_PHYSICAL_VECTOR).parent.mkdir(parents=True, exist_ok=True)
    np.save(OUT_PHYSICAL_VECTOR, physical_vector)

    saved_physical = np.load(OUT_PHYSICAL_VECTOR, mmap_mode="r")
    if saved_physical.shape != baseline.shape:
        raise SystemExit("physical vector is not MASCON-shape-compatible")

    physical_mean_mgal, physical_std_mgal = normalize_vector_file(OUT_PHYSICAL_VECTOR, OUT_NORMALIZED_VECTOR)

    if not math.isfinite(physical_mean_mgal) or not math.isfinite(physical_std_mgal):
        raise SystemExit("non-finite physical mean/std after finite-pass computation")

    baseline_metrics = pair_metrics(OUT_NORMALIZED_VECTOR, BASELINE)
    deficit_metrics = pair_metrics(OUT_NORMALIZED_VECTOR, DEFICIT)

    baseline_rmse = baseline_metrics["root_mean_square_delta"]
    deficit_rmse = deficit_metrics["root_mean_square_delta"]

    if abs(baseline_rmse - deficit_rmse) <= 1e-12:
        lower_rmse_model = "tie"
    elif baseline_rmse < deficit_rmse:
        lower_rmse_model = "baseline"
    else:
        lower_rmse_model = "deficit"

    prior = json.loads(PRIOR.read_text(encoding="utf-8"))

    artifact = {
        "object": "PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_2026_05_30",
        "status": "SOURCE_PHYSICAL_UNITS_OPERATOR_RECORDED_MASCON_UNIT_EQUIVALENCE_NOT_CLOSED",
        "source_physical_units_operator_recorded": True,
        "finite_physical_vector_statistics_verified": True,
        "source_output_units": "mGal radial gravity disturbance proxy",
        "source_to_grid_physical_units_calibrated": True,
        "source_to_mascon_shape_operator_recorded": True,
        "mascon_unit_equivalence_closed": False,
        "time_dependent_source_to_mascon_operator_closed": False,
        "comparison_metrics_recorded_on_normalized_alignment_vector": True,
        "source_name": SOURCE_NAME,
        "source_doi": SOURCE_DOI,
        "source_page": SOURCE_PAGE,
        "source_url_used": source_url_used,
        "source_gfc_path": str(GFC),
        "source_gfc_sha256": sha256_file(GFC),
        "physical_vector_path": str(OUT_PHYSICAL_VECTOR),
        "physical_vector_sha256": sha256_file(OUT_PHYSICAL_VECTOR),
        "normalized_alignment_vector_path": str(OUT_NORMALIZED_VECTOR),
        "normalized_alignment_vector_sha256": sha256_file(OUT_NORMALIZED_VECTOR),
        "physical_constants": {
            "earth_gravity_constant_m3_s2": gm,
            "reference_radius_m": a,
            "evaluation_radius_m": EVALUATION_RADIUS_M,
            "mgal_per_m_per_s2": MGAL_PER_M_PER_S2
        },
        "operator": {
            "input_format": "ICGEM .gfc fully-normalized spherical harmonic coefficients",
            "output_quantity": "radial gravity disturbance proxy",
            "output_units": "mGal",
            "max_degree_used": MAX_DEGREE_SYNTHESIS,
            "numeric_rows_seen": numeric_rows,
            "coefficient_count_used": len(coeffs),
            "synthesis_terms_used": used_terms,
            "raw_physical_grid_mean_mgal": raw_mean_mgal,
            "raw_physical_grid_std_mgal": raw_std_mgal,
            "physical_vector_mean_mgal_before_alignment_normalization": physical_mean_mgal,
            "physical_vector_std_mgal_before_alignment_normalization": physical_std_mgal,
            "source_header_modelname": header.get("modelname", "unknown"),
            "source_header_max_degree": header.get("max_degree", "unknown"),
            "source_header_norm": header.get("norm", "unknown"),
            "source_header_tide_system": header.get("tide_system", "unknown"),
            "token_prefixes_seen": token_prefixes,
            "grid": {
                "lat_count": lat_count,
                "lon_count": lon_count,
                "lat_centers_degrees": "uniform cell centers from -89.5 to 89.5",
                "lon_centers_degrees": "uniform cell centers from 0.5 to 359.5"
            },
            "time_index": {
                "time_count": time_count,
                "time_semantics": "static physical source grid broadcast to each MASCON time index"
            }
        },
        "normalized_alignment_comparison": {
            "baseline_metrics": baseline_metrics,
            "deficit_metrics": deficit_metrics,
            "lower_rmse_model": lower_rmse_model,
            "comparison_space": "dimensionless normalized alignment vector; not physical MASCON-unit equivalence"
        },
        "prior_gate": {
            "artifact": str(PRIOR),
            "status": prior.get("status", "unknown"),
            "current_lower_rmse_model": prior.get("current_lower_rmse_model", "unknown"),
            "physical_units_calibrated_source_to_mascon_operator_closed": prior.get("physical_units_calibrated_source_to_mascon_operator_closed", "unknown")
        },
        "missing_for_full_closure": [
            "MASCON vector physical units declaration",
            "absolute source-to-MASCON scaling law",
            "time-dependent source-to-MASCON operator",
            "validation of operator against independent physical-unit observations"
        ],
        "boundary": {
            "physical_source_units_operator_only": True,
            "mascon_unit_equivalence_not_closed": True,
            "time_dependent_operator_not_closed": True,
            "comparison_only": True,
            "no_empirical_gravity_result_claim": True,
            "no_gr_failure_claim": True,
            "no_new_gravity_claim": True,
            "no_dark_matter_replacement_claim": True,
            "no_lambda_cdm_failure_claim": True,
            "no_quantum_gravity_claim": True,
            "no_clay_claim": True,
            "independent_validation_required_before_physical_claim": True
        },
        "next_admissible_object": "MASCON_VECTOR_PHYSICAL_UNITS_DECLARATION_OR_TIME_DEPENDENT_SOURCE_TO_MASCON_OPERATOR"
    }

    OUT_ART.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    OUT_DOC.write_text(textwrap.dedent(f"""\
    # PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_2026_05_30

    Status: SOURCE_PHYSICAL_UNITS_OPERATOR_RECORDED_MASCON_UNIT_EQUIVALENCE_NOT_CLOSED.

    Source: {SOURCE_NAME}, DOI {SOURCE_DOI}.

    Source physical output units: mGal radial gravity disturbance proxy.

    Source-to-grid physical-units operator: recorded.

    Source-to-MASCON shape operator: recorded.

    MASCON unit equivalence: NOT_CLOSED.

    Time-dependent source-to-MASCON operator: NOT_CLOSED.

    Normalized alignment lower-RMSE model: `{lower_rmse_model}`.

    Baseline normalized-alignment RMSE: `{baseline_rmse}`.

    Deficit normalized-alignment RMSE: `{deficit_rmse}`.

    Boundary: physical source-units operator only. This does not assert empirical gravity validation, GR failure, new gravity, dark-matter replacement, Lambda-CDM failure, quantum gravity, or any Clay-problem claim. Full closure requires MASCON physical-unit declaration, absolute scaling, time-dependent mapping, and independent validation.
    """), encoding="utf-8")

    print(json.dumps({
        "status": artifact["status"],
        "source": SOURCE_NAME,
        "source_output_units": artifact["source_output_units"],
        "source_to_grid_physical_units_calibrated": True,
        "mascon_unit_equivalence_closed": False,
        "time_dependent_source_to_mascon_operator_closed": False,
        "physical_vector_sha256": sha256_file(OUT_PHYSICAL_VECTOR),
        "normalized_alignment_vector_sha256": sha256_file(OUT_NORMALIZED_VECTOR),
        "physical_vector_mean_mgal": physical_mean_mgal,
        "physical_vector_std_mgal": physical_std_mgal,
        "baseline_normalized_alignment_rmse": baseline_rmse,
        "deficit_normalized_alignment_rmse": deficit_rmse,
        "lower_rmse_model": lower_rmse_model,
        "vector_shape": list(saved_physical.shape),
        "vector_length": int(saved_physical.size)
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
