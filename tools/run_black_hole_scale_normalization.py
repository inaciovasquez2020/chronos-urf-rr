#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

G = 6.67430e-11
C = 299_792_458.0
M_SUN = 1.98847e30
AU_KM = 149_597_870.7
LIGHT_YEAR_KM = 9.4607304725808e12

RS_KM_PER_SOLAR_MASS = 2.0 * G * M_SUN / (C * C) / 1000.0


@dataclass(frozen=True)
class ScaleResult:
    label: str
    mass_solar: float
    rs_km: float
    domain_units: float
    domain_km: float
    domain_au: float
    domain_light_years: float
    passed: bool


def compute_scale(label: str, mass_solar: float, domain_units: float) -> ScaleResult:
    if mass_solar <= 0:
        raise ValueError("mass_solar must be positive")
    if domain_units <= 0:
        raise ValueError("domain_units must be positive")

    rs_km = RS_KM_PER_SOLAR_MASS * mass_solar
    domain_km = domain_units * rs_km

    return ScaleResult(
        label=label,
        mass_solar=mass_solar,
        rs_km=rs_km,
        domain_units=domain_units,
        domain_km=domain_km,
        domain_au=domain_km / AU_KM,
        domain_light_years=domain_km / LIGHT_YEAR_KM,
        passed=rs_km > 0 and domain_km > 0,
    )


def default_cases(domain_units: float) -> list[ScaleResult]:
    return [
        compute_scale("stellar_10_solar_mass", 10.0, domain_units),
        compute_scale("sagittarius_A_star_scale_4e6_solar_mass", 4.0e6, domain_units),
        compute_scale("m87_star_scale_6_5e9_solar_mass", 6.5e9, domain_units),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain-units", type=float, default=100.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rows = default_cases(args.domain_units)

    if args.json:
        print(json.dumps([asdict(row) for row in rows], indent=2, sort_keys=True))
    else:
        print("BLACK-HOLE SCALE NORMALIZATION MAP")
        print(f"r_s km per solar mass = {RS_KM_PER_SOLAR_MASS:.12f}")
        print(f"dimensionless domain = {args.domain_units} r_s")
        print()
        print(f"{'label':<42} {'M/Msun':>14} {'r_s km':>18} {'domain km':>18} {'domain AU':>14} {'domain ly':>14}")
        for row in rows:
            print(
                f"{row.label:<42} "
                f"{row.mass_solar:14.6e} "
                f"{row.rs_km:18.6e} "
                f"{row.domain_km:18.6e} "
                f"{row.domain_au:14.6e} "
                f"{row.domain_light_years:14.6e}"
            )
        print()
        print("PASS" if all(row.passed for row in rows) else "FAIL")

    return 0 if all(row.passed for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
