import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_black_hole_scale_normalization_verifier():
    subprocess.run(
        ["python3", "tools/verify_black_hole_scale_normalization_map.py"],
        cwd=ROOT,
        check=True,
    )

def test_black_hole_scale_normalization_values():
    proc = subprocess.run(
        ["python3", "tools/run_black_hole_scale_normalization.py", "--json"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    rows = json.loads(proc.stdout)
    by_label = {row["label"]: row for row in rows}

    stellar = by_label["stellar_10_solar_mass"]
    assert 29.5 < stellar["rs_km"] < 29.6
    assert 2953 < stellar["domain_km"] < 2954

    sgr = by_label["sagittarius_A_star_scale_4e6_solar_mass"]
    assert 1.18e7 < sgr["rs_km"] < 1.19e7
    assert 7.89 < sgr["domain_au"] < 7.91

    m87 = by_label["m87_star_scale_6_5e9_solar_mass"]
    assert 1.91e10 < m87["rs_km"] < 1.93e10
    assert 0.202 < m87["domain_light_years"] < 0.204

    assert all(row["passed"] for row in rows)
