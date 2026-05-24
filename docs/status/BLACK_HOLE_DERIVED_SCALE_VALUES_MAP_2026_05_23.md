# Black-Hole Derived Scale Values Map

Status: `DERIVED_SCALE_VALUES_ONLY_NOT_THEOREM_INPUT`

Dependencies:

- `BLACK_HOLE_SCALE_NORMALIZATION_MAP_2026_05_23`
- `FINITE_CAPACITY_OPTICAL_METRIC_NUMERICAL_WITNESS_2026_05_23`
- `FINITE_CAPACITY_OPTICAL_METRIC_SYMBOLIC_PROFILE_THEOREM_2026_05_23`

Executable:

- `tools/run_black_hole_derived_scale_values.py`

Value maps:

- `LIGHT_CROSSING_TIME_MAP`
- `HORIZON_AREA_MAP`
- `SURFACE_GRAVITY_MAP`
- `MEAN_DENSITY_MAP`
- `TIDAL_GRADIENT_MAP`
- `HAWKING_TEMPERATURE_MAP`
- `OPTICAL_DOMAIN_SWEEP_BY_MASS_MAP`

Formulas:

- light crossing time: `t_s = r_s/c` and `t_100 = 100 r_s/c`
- horizon area: `A = 4*pi*r_s^2`
- surface gravity: `kappa = c^4/(4GM)`
- mean density: `rho = 3M/(4*pi*r_s^3)`
- tidal gradient: `tidal scale = 2GM/r_s^3`
- Hawking temperature: `T_H = hbar*c^3/(8*pi*G*M*k_B)`
- optical domain sweep by mass: `domain = {10 r_s, 100 r_s, 1000 r_s}`

Masses:

- `10 M_sun`
- `4.0e6 M_sun`
- `6.5e9 M_sun`

Admissible use:

This map adds derived black-hole scale values to interpret finite-capacity optical metric profiles.

Verifier token: light crossing time.
Verifier token: horizon area.
Verifier token: surface gravity.
Verifier token: mean density.
Verifier token: tidal gradient.
Verifier token: Hawking temperature.
Verifier token: optical domain sweep by mass.
Verifier token: not a theorem input.

Boundary:

This does not prove gravity closure.
This does not prove the physical Einstein-matter flux identity.
This does not prove the restricted analytic estimate package assumptions.
This does not prove Chronos-RR.
This does not prove H4.1/FGL.
This does not prove P vs NP.
This does not prove any Clay problem.
