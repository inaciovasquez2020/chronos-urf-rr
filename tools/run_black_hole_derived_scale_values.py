from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass

G = 6.67430e-11
C = 299_792_458.0
M_SUN = 1.98847e30
AU_KM = 149_597_870.7
LIGHT_YEAR_KM = 9.4607304725808e12
HBAR = 1.054571817e-34
K_B = 1.380649e-23

RS_KM_PER_SOLAR_MASS = 2.0 * G * M_SUN / (C * C) / 1000.0


@dataclass(frozen=True)
class DomainScale:
    domain_rs: float
    domain_km: float
    domain_au: float
    domain_light_years: float


@dataclass(frozen=True)
class DerivedScaleRow:
    label: str
    mass_solar: float
    mass_kg: float
    rs_km: float
    rs_m: float
    light_crossing_time_s: float
    light_crossing_time_100rs_s: float
    horizon_area_m2: float
    surface_gravity_m_s2: float
    mean_density_kg_m3: float
    tidal_gradient_s2: float
    hawking_temperature_K: float
    optical_domain_sweep: list[DomainScale]
    passed: bool


def compute_row(label: str, mass_solar: float, domains_rs: list[float]) -> DerivedScaleRow:
    if mass_solar <= 0:
        raise ValueError("mass_solar must be positive")
    if any(d <= 0 for d in domains_rs):
        raise ValueError("all domain radii must be positive")

    mass_kg = mass_solar * M_SUN
    rs_m = 2.0 * G * mass_kg / (C * C)
    rs_km = rs_m / 1000.0

    light_crossing_time_s = rs_m / C
    light_crossing_time_100rs_s = 100.0 * light_crossing_time_s
    horizon_area_m2 = 4.0 * math.pi * rs_m * rs_m
    surface_gravity_m_s2 = C**4 / (4.0 * G * mass_kg)
    mean_density_kg_m3 = 3.0 * mass_kg / (4.0 * math.pi * rs_m**3)
    tidal_gradient_s2 = 2.0 * G * mass_kg / (rs_m**3)
    hawking_temperature_K = HBAR * C**3 / (8.0 * math.pi * G * mass_kg * K_B)

    sweep = []
    for d in domains_rs:
        domain_km = d * rs_km
        sweep.append(
            DomainScale(
                domain_rs=d,
                domain_km=domain_km,
                domain_au=domain_km / AU_KM,
                domain_light_years=domain_km / LIGHT_YEAR_KM,
            )
        )

    passed = all([
        mass_kg > 0,
        rs_m > 0,
        light_crossing_time_s > 0,
        light_crossing_time_100rs_s > light_crossing_time_s,
        horizon_area_m2 > 0,
        surface_gravity_m_s2 > 0,
        mean_density_kg_m3 > 0,
        tidal_gradient_s2 > 0,
        hawking_temperature_K > 0,
        all(x.domain_km > 0 for x in sweep),
    ])

    return DerivedScaleRow(
        label=label,
        mass_solar=mass_solar,
        mass_kg=mass_kg,
        rs_km=rs_km,
        rs_m=rs_m,
        light_crossing_time_s=light_crossing_time_s,
        light_crossing_time_100rs_s=light_crossing_time_100rs_s,
        horizon_area_m2=horizon_area_m2,
        surface_gravity_m_s2=surface_gravity_m_s2,
        mean_density_kg_m3=mean_density_kg_m3,
        tidal_gradient_s2=tidal_gradient_s2,
        hawking_temperature_K=hawking_temperature_K,
        optical_domain_sweep=sweep,
        passed=passed,
    )


def default_rows() -> list[DerivedScaleRow]:
    domains_rs = [10.0, 100.0, 1000.0]
    return [
        compute_row("stellar_10_solar_mass", 10.0, domains_rs),
        compute_row("sagittarius_A_star_scale_4e6_solar_mass", 4.0e6, domains_rs),
        compute_row("m87_star_scale_6_5e9_solar_mass", 6.5e9, domains_rs),
    ]


def row_to_dict(row: DerivedScaleRow) -> dict:
    data = asdict(row)
    data["optical_domain_sweep"] = [asdict(x) for x in row.optical_domain_sweep]
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rows = default_rows()

    if args.json:
        print(json.dumps([row_to_dict(row) for row in rows], indent=2, sort_keys=True))
    else:
        print("BLACK-HOLE DERIVED SCALE VALUES MAP")
        print(f"r_s km per solar mass = {RS_KM_PER_SOLAR_MASS:.12f}")
        print("domains = {10 r_s, 100 r_s, 1000 r_s}")
        print()
        print(
            f"{'label':<42} {'M/Msun':>14} {'r_s km':>14} {'t_s sec':>14} "
            f"{'t_100 sec':>14} {'area m^2':>14} {'kappa m/s^2':>14} "
            f"{'rho kg/m^3':>14} {'tidal s^-2':>14} {'T_H K':>14}"
        )
        for row in rows:
            print(
                f"{row.label:<42} "
                f"{row.mass_solar:14.6e} "
                f"{row.rs_km:14.6e} "
                f"{row.light_crossing_time_s:14.6e} "
                f"{row.light_crossing_time_100rs_s:14.6e} "
                f"{row.horizon_area_m2:14.6e} "
                f"{row.surface_gravity_m_s2:14.6e} "
                f"{row.mean_density_kg_m3:14.6e} "
                f"{row.tidal_gradient_s2:14.6e} "
                f"{row.hawking_temperature_K:14.6e}"
            )
        print()
        print("OPTICAL DOMAIN SWEEP")
        print(f"{'label':<42} {'domain r_s':>12} {'km':>16} {'AU':>16} {'ly':>16}")
        for row in rows:
            for domain in row.optical_domain_sweep:
                print(
                    f"{row.label:<42} "
                    f"{domain.domain_rs:12.1f} "
                    f"{domain.domain_km:16.6e} "
                    f"{domain.domain_au:16.6e} "
                    f"{domain.domain_light_years:16.6e}"
                )
        print()
        print("PASS" if all(row.passed for row in rows) else "FAIL")

    return 0 if all(row.passed for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
