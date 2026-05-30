#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import hashlib
import io
import json
import math
import os
import re
import textwrap
import zipfile
from collections import Counter

import numpy as np
from scipy.special import lpmv

DATE_TAG = "2026_05_30"

SOURCE_NAME = "XGM2019e_2159"
SOURCE_PAGE = "https://dataservices.gfz-potsdam.de/icgem/showshort.php?id=escidoc%3A4529896"
SOURCE_TOM = "https://icgem.gfz-potsdam.de/tom"
SOURCE_DOI = "10.5880/ICGEM.2019.007"

GFC = Path("external_data/xgm2019e/XGM2019e_2159.gfc")
BASELINE = Path("data/mascon_vectors/baseline_vector.npy")
DEFICIT = Path("data/mascon_vectors/deficit_vector.npy")

PRIOR_EIGEN6C4 = Path("artifacts/gravity/authentic_external_gravity_model_comparison_result_2026_05_30.json")
PRIOR_GOCO06S = Path("artifacts/gravity/independent_external_gravity_model_replication_or_public_holdout_validation_2026_05_30.json")
PRIOR_ITSG = Path("artifacts/gravity/second_independent_replication_or_physical_units_calibration_gate_2026_05_30.json")

OUT_VECTOR = Path(f"data/gravity_external_vectors/xgm2019e_2159_low_degree_static_mascon_compatible_vector_{DATE_TAG}.npy")
OUT_ART = Path(f"artifacts/gravity/physical_units_calibrated_source_to_mascon_operator_or_third_public_holdout_{DATE_TAG}.json")
OUT_MANIFEST = Path(f"artifacts/gravity/third_public_holdout_reproducibility_manifest_{DATE_TAG}.json")
OUT_DOC = Path(f"docs/status/PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_OR_THIRD_PUBLIC_HOLDOUT_{DATE_TAG}.md")

MAX_DEGREE_SYNTHESIS = int(os.environ.get("XGM2019E_SYNTHESIS_MAX_DEGREE", "24"))

STATIC_CANDIDATE_URLS = [
    "https://icgem.gfz-potsdam.de/getmodel/gfc/XGM2019e_2159.gfc",
    "https://icgem.gfz-potsdam.de/getmodel/zip/XGM2019e_2159.zip",
    "https://icgem.gfz.de/getmodel/gfc/XGM2019e_2159.gfc",
    "https://icgem.gfz.de/getmodel/zip/XGM2019e_2159.zip",
]

def request_bytes(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "chronos-urf-rr-validation/1.0"})
    with urlopen(req, timeout=240) as r:
        data = r.read()
    if data[:1] == b"<" and b"<html" in data[:2048].lower() and "tom" not in url and "showshort" not in url:
        raise ValueError(f"HTML returned from {url}")
    return data

def discover_model_urls() -> list[str]:
    html = request_bytes(SOURCE_TOM).decode("utf-8", errors="replace")
    urls = []

    for href in re.findall(r'href="([^"]+)"', html):
        h = href.replace("&amp;", "&")
        if "XGM2019e_2159" in h and ("getmodel" in h or ".gfc" in h or ".zip" in h):
            urls.append(urljoin(SOURCE_TOM, h))

    around = []
    idx = html.find("XGM2019e_2159")
    if idx >= 0:
        chunk = html[max(0, idx - 5000): idx + 5000]
        for href in re.findall(r'href="([^"]+)"', chunk):
            h = href.replace("&amp;", "&")
            if "getmodel" in h or ".gfc" in h or ".zip" in h:
                around.append(urljoin(SOURCE_TOM, h))

    return list(dict.fromkeys(urls + around + STATIC_CANDIDATE_URLS))

def download_gfc() -> str:
    GFC.parent.mkdir(parents=True, exist_ok=True)

    errors = []

    for url in discover_model_urls():
        try:
            data = request_bytes(url)

            if data[:4] == b"PK\x03\x04" or url.endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    names = [n for n in z.namelist() if n.lower().endswith(".gfc") and "xgm2019e_2159" in n.lower()]
                    if not names:
                        names = [n for n in z.namelist() if n.lower().endswith(".gfc") and "xgm2019e" in n.lower()]
                    if not names:
                        names = [n for n in z.namelist() if n.lower().endswith(".gfc")]
                    if not names:
                        raise ValueError("zip contained no .gfc file")
                    GFC.write_bytes(z.read(names[0]))
                    return url

            if b"end_of_head" in data[:500000] or b"gfc" in data[:500000]:
                GFC.write_bytes(data)
                return url

            errors.append((url, "no gfc marker"))
        except Exception as exc:
            errors.append((url, repr(exc)))

    raise RuntimeError("could not download XGM2019e_2159 .gfc; attempts=" + json.dumps(errors[-20:], indent=2))

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
            "no usable XGM2019e_2159 coefficients parsed; token prefixes="
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
        raise SystemExit(f"synthesized XGM2019e_2159 grid invalid: used={used}, mean={mean}, std={std}")

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
    for required in (BASELINE, DEFICIT, PRIOR_EIGEN6C4, PRIOR_GOCO06S, PRIOR_ITSG):
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
        raise SystemExit("saved XGM2019e_2159 vector is not shape-compatible with baseline")

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

    prior_eigen = json.loads(PRIOR_EIGEN6C4.read_text(encoding="utf-8"))
    prior_goco = json.loads(PRIOR_GOCO06S.read_text(encoding="utf-8"))
    prior_itsg = json.loads(PRIOR_ITSG.read_text(encoding="utf-8"))

    prior_lower_rmse_models = {
        "EIGEN-6C4": prior_eigen.get("lower_rmse_model", "unknown"),
        "GOCO06s": prior_goco.get("lower_rmse_model", "unknown"),
        "ITSG-Grace2018s": prior_itsg.get("current_lower_rmse_model", "unknown"),
    }

    agrees_with_prior_models = all(v == lower_rmse_model for v in prior_lower_rmse_models.values())

    manifest = {
        "object": "THIRD_PUBLIC_HOLDOUT_REPRODUCIBILITY_MANIFEST_2026_05_30",
        "status": "THIRD_PUBLIC_HOLDOUT_REPRODUCIBILITY_MANIFEST_RECORDED",
        "downloads": [
            {
                "source_name": SOURCE_NAME,
                "source_url_used": working_source_url,
                "source_page": SOURCE_PAGE,
                "source_tom": SOURCE_TOM,
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
            "physical_units_calibration_status": "NOT_CLOSED"
        },
        "boundary": {
            "third_public_holdout_only": True,
            "comparison_only": True,
            "physical_units_calibrated_operator_not_closed": True,
            "no_empirical_gravity_result_claim": True,
            "no_gr_failure_claim": True,
            "no_new_gravity_claim": True,
            "no_dark_matter_replacement_claim": True,
            "no_lambda_cdm_failure_claim": True,
            "no_quantum_gravity_claim": True,
            "no_clay_claim": True
        }
    }

    artifact = {
        "object": "PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_OR_THIRD_PUBLIC_HOLDOUT_2026_05_30",
        "status": "THIRD_PUBLIC_HOLDOUT_EXECUTED_PHYSICAL_UNITS_CALIBRATED_OPERATOR_NOT_CLOSED",
        "third_public_holdout_executed": True,
        "physical_units_calibrated_source_to_mascon_operator_closed": False,
        "source_to_mascon_operator_audit_recorded": True,
        "third_public_holdout_reproducibility_manifest_recorded": True,
        "comparison_result_interpretation_boundary_locked": True,
        "source_name": SOURCE_NAME,
        "source_kind": "combined global gravity field model; XGM2019e_2159 spherical harmonic expansion used as public holdout",
        "source_page": SOURCE_PAGE,
        "source_tom": SOURCE_TOM,
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
                "time_semantics": "static XGM2019e_2159 source broadcast to each MASCON time index"
            },
            "normalization": "zero mean and unit variance before comparison"
        },
        "physical_units_calibration_gate": {
            "calibration_status": "NOT_CLOSED",
            "source_units": "dimensionless normalized spherical-harmonic synthesis proxy after internal normalization",
            "mascon_units": "not asserted by this gate",
            "missing_for_closure": [
                "physical unit mapping from spherical harmonic functional to MASCON vector units",
                "absolute scale calibration",
                "time-dependent source-to-MASCON mapping instead of static broadcast",
                "independent validation in physical units"
            ]
        },
        "boundary": {
            "third_public_holdout_only": True,
            "comparison_only": True,
            "physical_units_calibrated_operator_not_closed": True,
            "no_empirical_gravity_result_claim": True,
            "no_gr_failure_claim": True,
            "no_new_gravity_claim": True,
            "no_dark_matter_replacement_claim": True,
            "no_lambda_cdm_failure_claim": True,
            "no_quantum_gravity_claim": True,
            "no_clay_claim": True,
            "independent_validation_required_before_physical_claim": True
        },
        "next_admissible_object": "PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR"
    }

    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUT_ART.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    OUT_DOC.write_text(textwrap.dedent(f"""\
    # PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_OR_THIRD_PUBLIC_HOLDOUT_2026_05_30

    Status: THIRD_PUBLIC_HOLDOUT_EXECUTED_PHYSICAL_UNITS_CALIBRATED_OPERATOR_NOT_CLOSED.

    Third public holdout source: {SOURCE_NAME}, DOI {SOURCE_DOI}.

    Prior lower-RMSE models:
    - EIGEN-6C4: `{prior_lower_rmse_models["EIGEN-6C4"]}`
    - GOCO06s: `{prior_lower_rmse_models["GOCO06s"]}`
    - ITSG-Grace2018s: `{prior_lower_rmse_models["ITSG-Grace2018s"]}`

    Current lower-RMSE model: `{lower_rmse_model}`.

    Agrees with prior lower-RMSE models: `{agrees_with_prior_models}`.

    Baseline RMSE: `{baseline_rmse}`.

    Deficit RMSE: `{deficit_rmse}`.

    Physical-units calibrated source-to-MASCON operator: NOT_CLOSED.

    Source-to-MASCON operator audit: recorded.

    Third public holdout reproducibility manifest: recorded.

    Interpretation boundary: comparison-only. This does not assert an empirical gravity result, GR failure, new gravity, dark-matter replacement, Lambda-CDM failure, quantum gravity, or any Clay-problem claim. A physical-units calibrated source-to-MASCON operator remains the next missing object.
    """), encoding="utf-8")

    print(json.dumps({
        "status": artifact["status"],
        "source": SOURCE_NAME,
        "source_doi": SOURCE_DOI,
        "source_url_used": working_source_url,
        "baseline_rmse": baseline_rmse,
        "deficit_rmse": deficit_rmse,
        "current_lower_rmse_model": lower_rmse_model,
        "prior_lower_rmse_models": prior_lower_rmse_models,
        "agrees_with_prior_lower_rmse_models": agrees_with_prior_models,
        "physical_units_calibrated_source_to_mascon_operator_closed": False,
        "numeric_rows_seen": numeric_rows,
        "synthesis_terms_used": used_coefficients,
        "raw_grid_std_before_normalization": raw_std,
        "vector_shape": list(saved.shape),
        "vector_length": int(saved.size),
        "external_vector_sha256": sha256_file(OUT_VECTOR)
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
