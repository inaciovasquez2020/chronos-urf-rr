#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import hashlib
import json
import math
import os
import re
import textwrap
from collections import Counter

import numpy as np
from scipy.special import lpmv

DATE_TAG = "2026_05_30"

SOURCE_NAME = "ITSG-Grace2018s"
SOURCE_PAGE = "https://dataservices.gfz-potsdam.de/icgem/showshort.php?id=escidoc%3A3600910"
SOURCE_DOI = "10.5880/ICGEM.2018.003"
SOURCE_STATIC_MODEL = "ITSG-Grace2018s"

SOURCE_CANDIDATE_URLS = [
    "https://icgem.gfz-potsdam.de/getmodel/gfc/cdcab005ac449315efdb79244dbd7a7f2426dff747305644f6d9e509843f3968/ITSG-Grace2018s.gfc",
    "https://icgem.gfz-potsdam.de/getmodel/zip/cdcab005ac449315efdb79244dbd7a7f2426dff747305644f6d9e509843f3968/ITSG-Grace2018s.zip",
]

GFC = Path("external_data/itsg_grace2018s/ITSG-Grace2018s.gfc")
BASELINE = Path("data/mascon_vectors/baseline_vector.npy")
DEFICIT = Path("data/mascon_vectors/deficit_vector.npy")
PRIOR_EIGEN = Path("artifacts/gravity/authentic_external_gravity_model_comparison_result_2026_05_30.json")
PRIOR_GOCO = Path("artifacts/gravity/independent_external_gravity_model_replication_or_public_holdout_validation_2026_05_30.json")

OUT_VECTOR = Path(f"data/gravity_external_vectors/itsg_grace2018s_low_degree_static_mascon_compatible_vector_{DATE_TAG}.npy")
OUT_ART = Path(f"artifacts/gravity/second_independent_replication_or_physical_units_calibration_gate_{DATE_TAG}.json")
OUT_MANIFEST = Path(f"artifacts/gravity/public_gravity_external_download_reproducibility_manifest_{DATE_TAG}.json")
OUT_DOC = Path(f"docs/status/SECOND_INDEPENDENT_REPLICATION_OR_PHYSICAL_UNITS_CALIBRATION_GATE_{DATE_TAG}.md")

MAX_DEGREE_SYNTHESIS = int(os.environ.get("ITSG_GRACE2018S_SYNTHESIS_MAX_DEGREE", "24"))

def request_bytes(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "chronos-urf-rr-validation/1.0"})
    with urlopen(req, timeout=180) as r:
        data = r.read()
    if data[:1] == b"<" and b"<html" in data[:1024].lower():
        raise ValueError(f"HTML returned from {url}")
    return data

def discover_gfc_url() -> str:
    req = Request(SOURCE_PAGE, headers={"User-Agent": "chronos-urf-rr-validation/1.0"})
    with urlopen(req, timeout=120) as r:
        html = r.read().decode("utf-8", errors="replace")

    candidates = []
    for href in re.findall(r'href="([^"]+)"', html):
        if "ITSG-Grace2018s" in href and ".gfc" in href:
            candidates.append(urljoin(SOURCE_PAGE, href.replace("&amp;", "&")))

    for href in candidates:
        try:
            data = request_bytes(href)
            if b"gfc" in data[:200000] or b"end_of_head" in data[:200000]:
                GFC.write_bytes(data)
                return href
        except Exception:
            continue

    raise RuntimeError("could not discover working ITSG-Grace2018s .gfc URL from source page")

def download_gfc() -> str:
    import io
    import zipfile

    GFC.parent.mkdir(parents=True, exist_ok=True)

    for url in SOURCE_CANDIDATE_URLS:
        try:
            data = request_bytes(url)
            if url.endswith(".zip") or data[:4] == b"PK\\x03\\x04":
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    names = [n for n in z.namelist() if n.endswith(".gfc") and "ITSG-Grace2018s" in n]
                    if not names:
                        raise ValueError("zip did not contain ITSG-Grace2018s .gfc")
                    GFC.write_bytes(z.read(names[0]))
                    return url
            if b"gfc" in data[:200000] or b"end_of_head" in data[:200000]:
                GFC.write_bytes(data)
                return url
        except Exception:
            pass

    return discover_gfc_url()

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
    if raw[:1] == b"<" or b"<html" in raw[:1024].lower():
        raise SystemExit("downloaded ITSG-Grace2018s file appears to be HTML, not GFC coefficients")

    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue

            parts = s.split()
            token_counts[parts[0]] += 1

            if len(parts) >= 2 and parts[0].lower() not in {"gfc", "gfct", "trnd", "acos", "asin"}:
                if not parts[0].lstrip("+-").isdigit():
                    header[parts[0]] = " ".join(parts[1:])

            rec = parts[0].lower()

            if rec in {"gfc", "gfct"} and len(parts) >= 5:
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
        raise SystemExit(
            "no usable ITSG-Grace2018s coefficients parsed; token prefixes="
            + json.dumps(dict(token_counts.most_common(20)), sort_keys=True)
        )

    return header, coeffs, numeric_rows, dict(token_counts.most_common(20))

def synthesize_static_grid(coeffs, lat_count: int, lon_count: int, max_degree: int):
    lats = np.linspace(-89.5, 89.5, lat_count, dtype=np.float64)
    lons = np.linspace(0.5, 359.5, lon_count, dtype=np.float64)

    phi = np.deg2rad(lons)
    sin_lat = np.sin(np.deg2rad(lats))

    grid = np.zeros((lat_count, lon_count), dtype=np.float64)

    used = 0
    for n in range(2, max_degree + 1):
        degree_scale = 1.0 / ((n + 1) ** 2)
        for m in range(0, n + 1):
            c, s = coeffs.get((n, m), (0.0, 0.0))
            if c == 0.0 and s == 0.0:
                continue
            pnm = lpmv(m, n, sin_lat)
            trig = c * np.cos(m * phi) + s * np.sin(m * phi)
            grid += degree_scale * np.outer(pnm, trig)
            used += 1

    grid = np.nan_to_num(grid, nan=0.0, posinf=0.0, neginf=0.0)

    mean = float(grid.mean())
    std = float(grid.std())

    if used == 0 or std == 0.0:
        raise SystemExit(f"synthesized ITSG-Grace2018s grid invalid: used={used}, mean={mean}, std={std}")

    return ((grid - mean) / std).astype(np.float32), used, mean, std

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
    for required in (BASELINE, DEFICIT, PRIOR_EIGEN, PRIOR_GOCO):
        if not required.exists():
            raise SystemExit(f"missing required file: {required}")

    working_source_url = download_gfc()

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

    header, coeffs, numeric_rows, token_prefixes = parse_gfc(GFC, MAX_DEGREE_SYNTHESIS)

    static_grid, used_coefficients, raw_mean, raw_std = synthesize_static_grid(
        coeffs=coeffs,
        lat_count=lat_count,
        lon_count=lon_count,
        max_degree=MAX_DEGREE_SYNTHESIS,
    )

    if baseline.ndim == 3:
        external = np.broadcast_to(static_grid, baseline.shape).astype(np.float32)
    else:
        external = np.broadcast_to(static_grid.reshape(-1), (time_count, lat_count * lon_count)).reshape(-1).astype(np.float32)

    np.save(OUT_VECTOR, external)

    saved = np.load(OUT_VECTOR, mmap_mode="r")
    if saved.shape != baseline.shape:
        raise SystemExit("saved ITSG-Grace2018s vector is not shape-compatible with baseline")

    baseline_metrics = pair_metrics(OUT_VECTOR, BASELINE)
    deficit_metrics = pair_metrics(OUT_VECTOR, DEFICIT)

    baseline_rmse = baseline_metrics["root_mean_square_delta"]
    deficit_rmse = deficit_metrics["root_mean_square_delta"]

    if abs(baseline_rmse - deficit_rmse) <= 1e-12:
        lower_rmse_model = "tie"
    elif baseline_rmse < deficit_rmse:
        lower_rmse_model = "baseline"
    else:
        lower_rmse_model = "deficit"

    prior_eigen = json.loads(PRIOR_EIGEN.read_text(encoding="utf-8"))
    prior_goco = json.loads(PRIOR_GOCO.read_text(encoding="utf-8"))

    prior_lower_rmse_models = {
        "EIGEN-6C4": prior_eigen.get("lower_rmse_model", "unknown"),
        "GOCO06s": prior_goco.get("lower_rmse_model", "unknown"),
    }

    agrees_with_prior_models = all(v == lower_rmse_model for v in prior_lower_rmse_models.values())

    manifest = {
        "object": "PUBLIC_GRAVITY_EXTERNAL_DOWNLOAD_REPRODUCIBILITY_MANIFEST_2026_05_30",
        "status": "PUBLIC_REPRODUCIBILITY_MANIFEST_RECORDED",
        "downloads": [
            {
                "source_name": SOURCE_NAME,
                "source_url_used": working_source_url,
                "source_page": SOURCE_PAGE,
                "source_doi": SOURCE_DOI,
                "local_path": str(GFC),
                "sha256": sha256_file(GFC),
                "bytes": GFC.stat().st_size
            }
        ],
        "generated_vectors": [
            {
                "source_name": SOURCE_NAME,
                "local_path": str(OUT_VECTOR),
                "sha256": sha256_file(OUT_VECTOR),
                "bytes": OUT_VECTOR.stat().st_size,
                "shape": list(saved.shape),
                "dtype": str(saved.dtype)
            }
        ],
        "operator": {
            "name": "LOW_DEGREE_STATIC_SPHERICAL_HARMONIC_TO_MASCON_COMPATIBLE_VECTOR_OPERATOR",
            "input": "ICGEM .gfc spherical harmonic coefficients",
            "max_degree_used": MAX_DEGREE_SYNTHESIS,
            "grid": f"{lat_count}x{lon_count} global cell-center grid",
            "normalization": "zero mean, unit variance",
            "time_mapping": f"static source broadcast across {time_count} MASCON time indices",
            "physical_units_calibration_status": "RECORDED_NOT_CLOSED"
        },
        "boundary": {
            "public_reproducibility_manifest_only": True,
            "comparison_only": True,
            "physical_units_calibration_not_closed": True,
            "no_empirical_gravity_result_claim": True,
            "no_gr_failure_claim": True,
            "no_new_gravity_claim": True,
            "no_dark_matter_replacement_claim": True,
            "no_lambda_cdm_failure_claim": True,
            "no_quantum_gravity_claim": True,
            "no_clay_claim": True
        }
    }

    result = {
        "object": "SECOND_INDEPENDENT_REPLICATION_OR_PHYSICAL_UNITS_CALIBRATION_GATE_2026_05_30",
        "status": "SECOND_INDEPENDENT_REPLICATION_EXECUTED_PHYSICAL_UNITS_CALIBRATION_GATE_RECORDED_NOT_CLOSED",
        "second_independent_replication_executed": True,
        "physical_units_calibration_gate_recorded": True,
        "physical_units_calibration_closed": False,
        "source_to_mascon_operator_audit_recorded": True,
        "public_reproducibility_manifest_recorded": True,
        "comparison_result_interpretation_boundary_locked": True,
        "source_name": SOURCE_NAME,
        "source_kind": "GRACE-only static gravity field solution",
        "source_page": SOURCE_PAGE,
        "source_url_used": working_source_url,
        "source_doi": SOURCE_DOI,
        "source_gfc_path": str(GFC),
        "source_gfc_sha256": sha256_file(GFC),
        "external_vector_path": str(OUT_VECTOR),
        "external_vector_sha256": sha256_file(OUT_VECTOR),
        "prior_lower_rmse_models": prior_lower_rmse_models,
        "current_lower_rmse_model": lower_rmse_model,
        "agrees_with_prior_lower_rmse_models": agrees_with_prior_models,
        "baseline_vector_path": str(BASELINE),
        "deficit_vector_path": str(DEFICIT),
        "baseline_metrics": baseline_metrics,
        "deficit_metrics": deficit_metrics,
        "vector_shape": list(saved.shape),
        "vector_length": int(saved.size),
        "source_to_mascon_operator_audit": {
            "input_format": "ICGEM .gfc spherical harmonic coefficients",
            "source_header_modelname": header.get("modelname", "unknown"),
            "source_header_max_degree": header.get("max_degree", "unknown"),
            "source_header_norm": header.get("norm", "unknown"),
            "source_header_tide_system": header.get("tide_system", "unknown"),
            "numeric_rows_seen": numeric_rows,
            "coefficient_count_used": len(coeffs),
            "synthesis_terms_used": used_coefficients,
            "max_degree_used": MAX_DEGREE_SYNTHESIS,
            "raw_grid_mean_before_normalization": raw_mean,
            "raw_grid_std_before_normalization": raw_std,
            "token_prefixes_seen": token_prefixes,
            "grid": {
                "lat_count": lat_count,
                "lon_count": lon_count,
                "lat_centers_degrees": "uniform cell centers from -89.5 to 89.5",
                "lon_centers_degrees": "uniform cell centers from 0.5 to 359.5"
            },
            "time_index": {
                "time_count": time_count,
                "time_semantics": "static ITSG-Grace2018s source broadcast to each MASCON time index"
            },
            "normalization": "zero mean and unit variance before comparison"
        },
        "physical_units_calibration_gate": {
            "source_units": "dimensionless normalized spherical-harmonic synthesis proxy after internal normalization",
            "mascon_units": "not asserted by this gate",
            "calibration_status": "RECORDED_NOT_CLOSED",
            "missing_for_closure": [
                "physical unit mapping from source functional to MASCON vector units",
                "absolute scale calibration",
                "time-dependent operator rather than static broadcast",
                "independent external validation in physical units"
            ]
        },
        "boundary": {
            "second_independent_replication_or_calibration_gate_only": True,
            "comparison_only": True,
            "physical_units_calibration_not_closed": True,
            "no_empirical_gravity_result_claim": True,
            "no_gr_failure_claim": True,
            "no_new_gravity_claim": True,
            "no_dark_matter_replacement_claim": True,
            "no_lambda_cdm_failure_claim": True,
            "no_quantum_gravity_claim": True,
            "no_clay_claim": True,
            "independent_validation_required_before_physical_claim": True
        },
        "next_admissible_object": "PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_OR_THIRD_PUBLIC_HOLDOUT"
    }

    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUT_ART.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    OUT_DOC.write_text(textwrap.dedent(f"""\
    # SECOND_INDEPENDENT_REPLICATION_OR_PHYSICAL_UNITS_CALIBRATION_GATE_2026_05_30

    Status: SECOND_INDEPENDENT_REPLICATION_EXECUTED_PHYSICAL_UNITS_CALIBRATION_GATE_RECORDED_NOT_CLOSED.

    Second independent source: {SOURCE_NAME}, DOI {SOURCE_DOI}.

    Prior lower-RMSE models:
    - EIGEN-6C4: `{prior_lower_rmse_models["EIGEN-6C4"]}`
    - GOCO06s: `{prior_lower_rmse_models["GOCO06s"]}`

    Current lower-RMSE model: `{lower_rmse_model}`.

    Agrees with prior lower-RMSE models: `{agrees_with_prior_models}`.

    Baseline RMSE: `{baseline_rmse}`.

    Deficit RMSE: `{deficit_rmse}`.

    Physical-units calibration status: RECORDED_NOT_CLOSED.

    Source-to-MASCON operator audit: recorded.

    Public reproducibility manifest: recorded.

    Interpretation boundary: comparison-only. This does not assert an empirical gravity result, GR failure, new gravity, dark-matter replacement, Lambda-CDM failure, quantum gravity, or any Clay-problem claim. Physical-units calibration and independent validation remain required before any physical claim.
    """), encoding="utf-8")

    print(json.dumps({
        "status": result["status"],
        "source": SOURCE_NAME,
        "source_doi": SOURCE_DOI,
        "source_url_used": working_source_url,
        "baseline_rmse": baseline_rmse,
        "deficit_rmse": deficit_rmse,
        "current_lower_rmse_model": lower_rmse_model,
        "prior_lower_rmse_models": prior_lower_rmse_models,
        "agrees_with_prior_lower_rmse_models": agrees_with_prior_models,
        "physical_units_calibration_closed": False,
        "numeric_rows_seen": numeric_rows,
        "synthesis_terms_used": used_coefficients,
        "raw_grid_std_before_normalization": raw_std,
        "vector_shape": list(saved.shape),
        "vector_length": int(saved.size),
        "external_vector_sha256": sha256_file(OUT_VECTOR)
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
