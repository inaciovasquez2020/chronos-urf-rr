# GfE axial 221 epsilon-continuation certificate — 2026-09-25

Status: **certified within the stated projected massless order-reduced branch**.

## Result

For the projected axial `(ell,m,n) = (2,2,1)` mode with

`ε = β²/M⁴ ∈ [0, 10⁻⁴]`,

the verifier certifies exactly one quasinormal-mode root, counting multiplicity, in the moving disk

`|Ω - Ω_pred(ε)| ≤ 5 × 10⁻⁶`,

with affine predictor

`Ω_pred(ε) = Ω₀ + s ε`,

`Ω₀ = 0.34671099687810464 - 0.27391487535351056 i`,

`s = 0.0196971854 - 0.0671226649 i`.

Because the zero count is one for every ε in the interval, the enclosed root is simple throughout the certified tube.

## Decisive bounds

`q_hor ≤ 0.7138198542173089 < 1`

`δ_infinity ≥ 0.589385874169097 > 0`

`R_horizon ≤ 1.4895778040996383 × 10⁻⁵`

`R_infinity ≤ 1.7613920193161312 × 10⁻⁵`

`Rouché linear lower = 1.0336399695740086 × 10⁻⁴`

`Rouché error upper = 2.41823809093891 × 10⁻⁵`

`Rouché margin ≥ 7.918161604801174 × 10⁻⁵ > 0`.

## Certified chain

The standalone verifier checks:

- the shifted-horizon ε-linear cleared Frobenius recurrence;
- an all-orders weighted horizon coefficient majorant;
- a 96-bit fixed-point two-direction affine model carrying both the root-disk and ε directions;
- separate nonlinear-remainder transport along the horizon Riccati flow;
- an ε-dependent outgoing Laurent-Jost endpoint and vertical-ray Volterra tail enclosure;
- separate nonlinear-remainder transport along the infinity Riccati flow; and
- the uniform Rouché boundary inequality around the affine frequency predictor.

## Exact claim boundary

The predictor slope is a **certified tube-center choice**. This certificate does **not** independently enclose

`dΩ_221/dε |_(ε=0)`

as a derivative value.

It also does not certify the polar sector, axial-polar splitting, or the full unreduced trace-log spectrum, and it does not establish full gravity closure or observational detectability.

## Repository anchors

- verifier: `tools/gfe/verify_gfe_axial_221_epsilon_continuation.py`
- certificate: `artifacts/chronos/gfe_axial_221_epsilon_continuation_certificate.json`
- regression test: `tests/test_gfe_axial_221_epsilon_continuation.py`
