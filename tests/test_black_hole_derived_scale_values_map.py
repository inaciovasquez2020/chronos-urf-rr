import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_black_hole_derived_scale_values_verifier():
    subprocess.run(
        ["python3", "tools/verify_black_hole_derived_scale_values_map.py"],
        cwd=ROOT,
        check=True,
    )

def test_black_hole_derived_scale_values_runner():
    proc = subprocess.run(
        ["python3", "tools/run_black_hole_derived_scale_values.py", "--json"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    rows = json.loads(proc.stdout)
    assert len(rows) == 3
    assert all(row["passed"] for row in rows)

    by_label = {row["label"]: row for row in rows}

    stellar = by_label["stellar_10_solar_mass"]
    sgr = by_label["sagittarius_A_star_scale_4e6_solar_mass"]
    m87 = by_label["m87_star_scale_6_5e9_solar_mass"]

    assert 29.5 < stellar["rs_km"] < 29.6
    assert 0.0098 < stellar["light_crossing_time_100rs_s"] < 0.0099

    assert 7.89 < sgr["optical_domain_sweep"][1]["domain_au"] < 7.91
    assert 0.202 < m87["optical_domain_sweep"][1]["domain_light_years"] < 0.204

    assert stellar["surface_gravity_m_s2"] > sgr["surface_gravity_m_s2"] > m87["surface_gravity_m_s2"]
    assert stellar["mean_density_kg_m3"] > sgr["mean_density_kg_m3"] > m87["mean_density_kg_m3"]
    assert stellar["tidal_gradient_s2"] > sgr["tidal_gradient_s2"] > m87["tidal_gradient_s2"]
    assert stellar["hawking_temperature_K"] > sgr["hawking_temperature_K"] > m87["hawking_temperature_K"]

    for row in rows:
        domains = row["optical_domain_sweep"]
        assert [d["domain_rs"] for d in domains] == [10.0, 100.0, 1000.0]
        assert domains[0]["domain_km"] < domains[1]["domain_km"] < domains[2]["domain_km"]
