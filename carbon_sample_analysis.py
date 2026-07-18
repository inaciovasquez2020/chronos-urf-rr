#!/usr/bin/env python3
"""Strict same-specimen carbon profile analysis.

This module does not synthesize measurement data.  It validates calibrated
metadata plus CT-density and residual-stress arrays, runs the merged nonlinear
radial model at multiple input resolutions, propagates declared measurement
uncertainties, and reports a conditional universal/massless/long-range scalar
no-go estimate.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
import unittest
from tempfile import TemporaryDirectory

import numpy as np

from toy_gravity import (
    DimensionlessRadialCarbonModel,
    MeasuredCarbonProfiles,
    normalization_compatible_no_go_acceleration,
)

G_SI = 6.67430e-11
C_SI = 299_792_458.0
Q_C_TOY_J = 0.1
FORBIDDEN_MARKERS = {
    "",
    "pending",
    "placeholder",
    "proposed",
    "unknown",
    "tbd",
    "n/a",
    "na",
    "none",
    "null",
}


@dataclass(frozen=True)
class SampleMetadata:
    sample_id: str
    material: str
    measurement_status: str
    shape: str
    mass_kg: float
    mass_uncertainty_kg: float
    radius_m: float
    radius_uncertainty_m: float
    temperature_k: float
    temperature_uncertainty_k: float
    observer_radius_m: float
    observer_radius_uncertainty_m: float
    ct_instrument: str
    ct_calibration_id: str
    ct_calibration_date: str
    density_calibration_method: str
    stress_instrument: str
    stress_calibration_id: str
    stress_calibration_date: str
    acquisition_timestamp: str
    provenance: str

    @staticmethod
    def _required_text(data: dict[str, Any], key: str) -> str:
        value = str(data.get(key, "")).strip()
        if value.lower() in FORBIDDEN_MARKERS:
            raise ValueError(f"{key} must contain measured provenance")
        return value

    @staticmethod
    def _required_positive(data: dict[str, Any], key: str) -> float:
        try:
            value = float(data[key])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"{key} must be numeric") from error
        if not math.isfinite(value) or value <= 0.0:
            raise ValueError(f"{key} must be finite and positive")
        return value

    @staticmethod
    def _required_nonnegative(data: dict[str, Any], key: str) -> float:
        try:
            value = float(data[key])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"{key} must be numeric") from error
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"{key} must be finite and nonnegative")
        return value

    @classmethod
    def from_json(cls, path: Path) -> "SampleMetadata":
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            raise ValueError("sample metadata must be a JSON object")

        status = cls._required_text(data, "measurement_status")
        if status.upper() != "MEASURED":
            raise ValueError("measurement_status must equal MEASURED")
        shape = cls._required_text(data, "shape")
        if shape.lower() != "sphere":
            raise ValueError("the current radial solver requires shape=sphere")

        metadata = cls(
            sample_id=cls._required_text(data, "sample_id"),
            material=cls._required_text(data, "material"),
            measurement_status=status,
            shape=shape,
            mass_kg=cls._required_positive(data, "mass_kg"),
            mass_uncertainty_kg=cls._required_nonnegative(
                data, "mass_uncertainty_kg"
            ),
            radius_m=cls._required_positive(data, "radius_m"),
            radius_uncertainty_m=cls._required_nonnegative(
                data, "radius_uncertainty_m"
            ),
            temperature_k=cls._required_positive(data, "temperature_k"),
            temperature_uncertainty_k=cls._required_nonnegative(
                data, "temperature_uncertainty_k"
            ),
            observer_radius_m=cls._required_positive(
                data, "observer_radius_m"
            ),
            observer_radius_uncertainty_m=cls._required_nonnegative(
                data, "observer_radius_uncertainty_m"
            ),
            ct_instrument=cls._required_text(data, "ct_instrument"),
            ct_calibration_id=cls._required_text(
                data, "ct_calibration_id"
            ),
            ct_calibration_date=cls._required_text(
                data, "ct_calibration_date"
            ),
            density_calibration_method=cls._required_text(
                data, "density_calibration_method"
            ),
            stress_instrument=cls._required_text(data, "stress_instrument"),
            stress_calibration_id=cls._required_text(
                data, "stress_calibration_id"
            ),
            stress_calibration_date=cls._required_text(
                data, "stress_calibration_date"
            ),
            acquisition_timestamp=cls._required_text(
                data, "acquisition_timestamp"
            ),
            provenance=cls._required_text(data, "provenance"),
        )

        for key, value in (
            ("ct_calibration_date", metadata.ct_calibration_date),
            ("stress_calibration_date", metadata.stress_calibration_date),
            ("acquisition_timestamp", metadata.acquisition_timestamp),
        ):
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError as error:
                raise ValueError(f"{key} must be ISO-8601") from error

        if metadata.observer_radius_m <= metadata.radius_m:
            raise ValueError("observer_radius_m must exceed sample radius_m")
        return metadata


@dataclass(frozen=True)
class MeasurementBundle:
    metadata: SampleMetadata
    profiles: MeasuredCarbonProfiles
    density_uncertainty_kg_m3: np.ndarray
    radial_stress_uncertainty_pa: np.ndarray
    tangential_stress_uncertainty_pa: np.ndarray
    metadata_sha256: str
    ct_sha256: str
    stress_sha256: str


@dataclass(frozen=True)
class ConvergenceLevel:
    points: int
    outer_radius_ratio: float
    mass_kg: float
    trace_energy_j: float
    beta_c: float
    acceleration_m_s2: float
    surface_chi: float


@dataclass(frozen=True)
class UncertaintySummary:
    draws: int
    seed: int
    mean_m_s2: float
    standard_deviation_m_s2: float
    minimum_m_s2: float
    maximum_m_s2: float
    quantile_025_m_s2: float
    median_m_s2: float
    quantile_975_m_s2: float


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_numeric_csv(
    path: Path,
    required_columns: Iterable[str],
) -> dict[str, np.ndarray]:
    required = tuple(required_columns)
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no CSV header")
        missing = [name for name in required if name not in reader.fieldnames]
        if missing:
            raise ValueError(f"{path} missing columns: {', '.join(missing)}")
        columns: dict[str, list[float]] = {name: [] for name in required}
        for line_number, row in enumerate(reader, start=2):
            for name in required:
                raw = str(row.get(name, "")).strip()
                if raw.lower() in FORBIDDEN_MARKERS:
                    raise ValueError(
                        f"{path}:{line_number}:{name} is not measured"
                    )
                try:
                    value = float(raw)
                except ValueError as error:
                    raise ValueError(
                        f"{path}:{line_number}:{name} must be numeric"
                    ) from error
                if not math.isfinite(value):
                    raise ValueError(
                        f"{path}:{line_number}:{name} must be finite"
                    )
                columns[name].append(value)

    arrays = {name: np.asarray(values, dtype=float) for name, values in columns.items()}
    if any(array.size < 4 for array in arrays.values()):
        raise ValueError(f"{path} requires at least four measured rows")
    return arrays


def load_measurement_bundle(
    metadata_path: Path,
    ct_path: Path,
    stress_path: Path,
) -> MeasurementBundle:
    metadata = SampleMetadata.from_json(metadata_path)
    ct = _read_numeric_csv(
        ct_path,
        ("r_m", "rho_kg_m3", "rho_uncertainty_kg_m3"),
    )
    stress = _read_numeric_csv(
        stress_path,
        (
            "r_m",
            "sigma_rr_pa",
            "sigma_tt_pa",
            "sigma_rr_uncertainty_pa",
            "sigma_tt_uncertainty_pa",
        ),
    )

    if np.any(ct["rho_kg_m3"] <= 0.0):
        raise ValueError("CT density values must be positive")
    for name in (
        "rho_uncertainty_kg_m3",
        "sigma_rr_uncertainty_pa",
        "sigma_tt_uncertainty_pa",
    ):
        source = ct if name.startswith("rho") else stress
        if np.any(source[name] < 0.0):
            raise ValueError(f"{name} must be nonnegative")

    profiles = MeasuredCarbonProfiles(
        ct["r_m"],
        ct["rho_kg_m3"],
        stress["r_m"],
        stress["sigma_rr_pa"],
        stress["sigma_tt_pa"],
    )

    mass_tolerance = max(5.0 * metadata.mass_uncertainty_kg, 1.0e-12)
    if abs(profiles.mass_kg() - metadata.mass_kg) > mass_tolerance:
        raise ValueError(
            "integrated CT mass disagrees with metadata mass by more than 5 sigma"
        )
    radius_tolerance = max(5.0 * metadata.radius_uncertainty_m, 1.0e-12)
    if abs(profiles.radius_m - metadata.radius_m) > radius_tolerance:
        raise ValueError(
            "profile radius disagrees with metadata radius by more than 5 sigma"
        )

    return MeasurementBundle(
        metadata=metadata,
        profiles=profiles,
        density_uncertainty_kg_m3=ct["rho_uncertainty_kg_m3"],
        radial_stress_uncertainty_pa=stress[
            "sigma_rr_uncertainty_pa"
        ],
        tangential_stress_uncertainty_pa=stress[
            "sigma_tt_uncertainty_pa"
        ],
        metadata_sha256=_sha256(metadata_path),
        ct_sha256=_sha256(ct_path),
        stress_sha256=_sha256(stress_path),
    )


def _resample_profiles(
    bundle: MeasurementBundle,
    points: int,
) -> MeasuredCarbonProfiles:
    if points < 4:
        raise ValueError("convergence level requires at least four points")
    radius = np.linspace(0.0, bundle.profiles.radius_m, points)
    return MeasuredCarbonProfiles(
        radius,
        bundle.profiles.density(radius),
        radius,
        bundle.profiles.radial_stress(radius),
        bundle.profiles.tangential_stress(radius),
    )


def run_convergence_study(
    bundle: MeasurementBundle,
    point_levels: tuple[int, ...] = (65, 129, 257),
    outer_radius_ratios: tuple[float, ...] = (10.0, 20.0, 40.0),
) -> list[ConvergenceLevel]:
    if len(point_levels) != len(outer_radius_ratios):
        raise ValueError("point and exterior-domain levels must have equal length")
    if tuple(sorted(point_levels)) != point_levels:
        raise ValueError("point levels must be increasing")
    if tuple(sorted(outer_radius_ratios)) != outer_radius_ratios:
        raise ValueError("outer-radius ratios must be increasing")

    levels: list[ConvergenceLevel] = []
    for points, outer_ratio in zip(point_levels, outer_radius_ratios):
        model = DimensionlessRadialCarbonModel(
            _resample_profiles(bundle, points),
            q_c_toy_j=Q_C_TOY_J,
            outer_radius_ratio=outer_ratio,
        ).solve()
        state = model.fields(1.0)
        acceleration = model.universal_long_range_acceleration_difference(
            bundle.metadata.observer_radius_m
        )
        levels.append(
            ConvergenceLevel(
                points=points,
                outer_radius_ratio=outer_ratio,
                mass_kg=model.mass_kg,
                trace_energy_j=model.trace_energy_j,
                beta_c=model.beta_c,
                acceleration_m_s2=acceleration,
                surface_chi=float(state[2]),
            )
        )
    return levels


def _interp_uncertainty(
    source_radius: np.ndarray,
    source_uncertainty: np.ndarray,
    target_radius: np.ndarray,
) -> np.ndarray:
    return np.interp(target_radius, source_radius, source_uncertainty)


def propagate_uncertainty(
    bundle: MeasurementBundle,
    *,
    draws: int = 10_000,
    seed: int = 20260718,
) -> UncertaintySummary:
    if draws < 100:
        raise ValueError("draws must be at least 100")
    rng = np.random.default_rng(seed)

    radius_grid = np.unique(
        np.concatenate(
            (
                bundle.profiles.ct_radius_m,
                bundle.profiles.stress_radius_m,
            )
        )
    )
    density = bundle.profiles.density(radius_grid)
    radial_stress = bundle.profiles.radial_stress(radius_grid)
    tangential_stress = bundle.profiles.tangential_stress(radius_grid)
    density_sigma = _interp_uncertainty(
        bundle.profiles.ct_radius_m,
        bundle.density_uncertainty_kg_m3,
        radius_grid,
    )
    radial_sigma = _interp_uncertainty(
        bundle.profiles.stress_radius_m,
        bundle.radial_stress_uncertainty_pa,
        radius_grid,
    )
    tangential_sigma = _interp_uncertainty(
        bundle.profiles.stress_radius_m,
        bundle.tangential_stress_uncertainty_pa,
        radius_grid,
    )

    accelerations = np.empty(draws, dtype=float)
    chunk_size = 256
    for start in range(0, draws, chunk_size):
        stop = min(start + chunk_size, draws)
        count = stop - start
        radius_scale = rng.normal(
            1.0,
            bundle.metadata.radius_uncertainty_m / bundle.metadata.radius_m,
            size=count,
        )
        observer_radius = rng.normal(
            bundle.metadata.observer_radius_m,
            bundle.metadata.observer_radius_uncertainty_m,
            size=count,
        )
        if np.any(radius_scale <= 0.0) or np.any(
            observer_radius <= bundle.metadata.radius_m
        ):
            raise ValueError("declared radius uncertainty permits invalid geometry")

        sampled_density = rng.normal(
            density,
            density_sigma,
            size=(count, radius_grid.size),
        )
        if np.any(sampled_density <= 0.0):
            raise ValueError(
                "declared density uncertainty permits nonpositive density"
            )
        sampled_radial = rng.normal(
            radial_stress,
            radial_sigma,
            size=(count, radius_grid.size),
        )
        sampled_tangential = rng.normal(
            tangential_stress,
            tangential_sigma,
            size=(count, radius_grid.size),
        )

        scaled_radius = radius_grid[None, :] * radius_scale[:, None]
        shell_mass_integrand = scaled_radius**2 * sampled_density
        mass = 4.0 * math.pi * np.trapezoid(
            shell_mass_integrand,
            scaled_radius,
            axis=1,
        )
        trace_density = (
            sampled_density * C_SI**2
            - sampled_radial
            - 2.0 * sampled_tangential
        )
        trace_energy = 4.0 * math.pi * np.trapezoid(
            scaled_radius**2 * trace_density,
            scaled_radius,
            axis=1,
        )
        if np.any(trace_energy <= 0.0):
            raise ValueError(
                "declared uncertainty permits nonpositive trace energy"
            )
        accelerations[start:stop] = (
            2.0
            * (Q_C_TOY_J / trace_energy) ** 2
            * G_SI
            * mass
            / observer_radius**2
        )

    q025, median, q975 = np.quantile(
        accelerations,
        (0.025, 0.5, 0.975),
    )
    return UncertaintySummary(
        draws=draws,
        seed=seed,
        mean_m_s2=float(np.mean(accelerations)),
        standard_deviation_m_s2=float(np.std(accelerations, ddof=1)),
        minimum_m_s2=float(np.min(accelerations)),
        maximum_m_s2=float(np.max(accelerations)),
        quantile_025_m_s2=float(q025),
        median_m_s2=float(median),
        quantile_975_m_s2=float(q975),
    )


def analyze_sample(
    metadata_path: Path,
    ct_path: Path,
    stress_path: Path,
    *,
    draws: int,
    seed: int,
) -> dict[str, Any]:
    bundle = load_measurement_bundle(metadata_path, ct_path, stress_path)
    convergence = run_convergence_study(bundle)
    uncertainty = propagate_uncertainty(bundle, draws=draws, seed=seed)

    finest = convergence[-1]
    previous = convergence[-2]
    convergence_absolute = abs(
        finest.acceleration_m_s2 - previous.acceleration_m_s2
    )
    convergence_relative = (
        convergence_absolute / abs(finest.acceleration_m_s2)
        if finest.acceleration_m_s2 != 0.0
        else math.inf
    )
    total_sigma = math.hypot(
        uncertainty.standard_deviation_m_s2,
        convergence_absolute,
    )
    five_sigma_upper = abs(finest.acceleration_m_s2) + 5.0 * total_sigma

    independently_recomputed = normalization_compatible_no_go_acceleration(
        Q_C_TOY_J,
        finest.trace_energy_j,
        finest.mass_kg,
        bundle.metadata.observer_radius_m,
        G_SI,
    )
    if not math.isclose(
        independently_recomputed,
        finest.acceleration_m_s2,
        rel_tol=1.0e-12,
        abs_tol=0.0,
    ):
        raise RuntimeError("independent no-go recomputation disagrees")

    return {
        "result": "conditional sample-specific no-go estimate computed",
        "physical_status": "CONDITIONAL",
        "assumptions": [
            "universal scalar source and detector coupling",
            "massless long-range scalar",
            "spherical radial reduction",
            "declared point uncertainties treated as independent Gaussian inputs",
        ],
        "boundary": (
            "not interval-certified; temperature metadata is recorded but no "
            "thermal constitutive coefficient is supplied to the field model"
        ),
        "sample_metadata": asdict(bundle.metadata),
        "input_hashes_sha256": {
            "metadata": bundle.metadata_sha256,
            "ct_density": bundle.ct_sha256,
            "residual_stress": bundle.stress_sha256,
        },
        "convergence_levels": [asdict(level) for level in convergence],
        "convergence_absolute_m_s2": convergence_absolute,
        "convergence_relative": convergence_relative,
        "uncertainty": asdict(uncertainty),
        "conditional_no_go_acceleration_m_s2": finest.acceleration_m_s2,
        "combined_standard_uncertainty_m_s2": total_sigma,
        "conditional_five_sigma_upper_m_s2": five_sigma_upper,
        "normalization_map": "Q_C_TOY = BETA_C * E_TR",
        "q_c_toy_j": Q_C_TOY_J,
    }


def _write_fixture(directory: Path) -> tuple[Path, Path, Path]:
    radius = np.linspace(0.0, 0.02, 33)
    density = np.full_like(radius, 1500.0)
    stress = np.zeros_like(radius)
    mass = float(
        4.0 * math.pi * np.trapezoid(radius**2 * density, radius)
    )

    metadata = {
        "sample_id": "SYNTHETIC-UNIT-TEST",
        "material": "synthetic carbon test fixture",
        "measurement_status": "MEASURED",
        "shape": "sphere",
        "mass_kg": mass,
        "mass_uncertainty_kg": max(mass * 1.0e-6, 1.0e-12),
        "radius_m": float(radius[-1]),
        "radius_uncertainty_m": 1.0e-9,
        "temperature_k": 293.15,
        "temperature_uncertainty_k": 0.01,
        "observer_radius_m": 1.0,
        "observer_radius_uncertainty_m": 1.0e-6,
        "ct_instrument": "synthetic fixture generator",
        "ct_calibration_id": "TEST-CT-001",
        "ct_calibration_date": "2026-07-18",
        "density_calibration_method": "synthetic exact fixture",
        "stress_instrument": "synthetic fixture generator",
        "stress_calibration_id": "TEST-STRESS-001",
        "stress_calibration_date": "2026-07-18",
        "acquisition_timestamp": "2026-07-18T12:00:00Z",
        "provenance": "SYNTHETIC_TEST_FIXTURE_NOT_PHYSICAL_DATA",
    }
    metadata_path = directory / "sample_metadata.json"
    metadata_path.write_text(json.dumps(metadata))

    ct_path = directory / "ct_density.csv"
    with ct_path.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            ("r_m", "rho_kg_m3", "rho_uncertainty_kg_m3")
        )
        for r, rho in zip(radius, density):
            writer.writerow((r, rho, 0.01))

    stress_path = directory / "residual_stress.csv"
    with stress_path.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            (
                "r_m",
                "sigma_rr_pa",
                "sigma_tt_pa",
                "sigma_rr_uncertainty_pa",
                "sigma_tt_uncertainty_pa",
            )
        )
        for r, rr, tt in zip(radius, stress, stress):
            writer.writerow((r, rr, tt, 0.01, 0.01))
    return metadata_path, ct_path, stress_path


class CarbonSampleAnalysisTests(unittest.TestCase):
    def test_placeholder_metadata_is_rejected(self) -> None:
        with TemporaryDirectory() as raw:
            directory = Path(raw)
            metadata_path, _, _ = _write_fixture(directory)
            data = json.loads(metadata_path.read_text())
            data["ct_calibration_id"] = "PENDING"
            metadata_path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                SampleMetadata.from_json(metadata_path)

    def test_bundle_convergence_and_uncertainty(self) -> None:
        with TemporaryDirectory() as raw:
            directory = Path(raw)
            metadata_path, ct_path, stress_path = _write_fixture(directory)
            bundle = load_measurement_bundle(
                metadata_path,
                ct_path,
                stress_path,
            )
            levels = run_convergence_study(
                bundle,
                point_levels=(17, 25, 33),
                outer_radius_ratios=(5.0, 7.0, 9.0),
            )
            self.assertEqual(len(levels), 3)
            self.assertGreater(levels[-1].acceleration_m_s2, 0.0)
            uncertainty = propagate_uncertainty(
                bundle,
                draws=128,
                seed=7,
            )
            self.assertGreater(uncertainty.mean_m_s2, 0.0)
            self.assertGreaterEqual(
                uncertainty.standard_deviation_m_s2,
                0.0,
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--ct-density", type=Path)
    parser.add_argument("--residual-stress", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--draws", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20260718)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(
            CarbonSampleAnalysisTests
        )
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(0 if result.wasSuccessful() else 1)

    required = {
        "--metadata": args.metadata,
        "--ct-density": args.ct_density,
        "--residual-stress": args.residual_stress,
        "--output": args.output,
    }
    missing = [name for name, value in required.items() if value is None]
    if missing:
        parser.error("required arguments: " + ", ".join(missing))

    report = analyze_sample(
        args.metadata,
        args.ct_density,
        args.residual_stress,
        draws=args.draws,
        seed=args.seed,
    )
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("RESULT := conditional sample-specific no-go estimate computed")
    print(
        "CONDITIONAL_NO_GO_ACCELERATION_M_PER_S2 := "
        f"{report['conditional_no_go_acceleration_m_s2']:.16g}"
    )
    print(
        "COMBINED_STANDARD_UNCERTAINTY_M_PER_S2 := "
        f"{report['combined_standard_uncertainty_m_s2']:.16g}"
    )
    print(
        "CONDITIONAL_FIVE_SIGMA_UPPER_M_PER_S2 := "
        f"{report['conditional_five_sigma_upper_m_s2']:.16g}"
    )
    print(f"OUTPUT := {args.output}")
    print(
        "BOUNDARY := conditional universal massless long-range scalar model; "
        "not interval-certified"
    )


if __name__ == "__main__":
    main()
