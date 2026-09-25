# GfE axial 221 epsilon-zero simple-root certificate — 2026-09-24

Status: **certified within the stated epsilon-zero projected branch**.

## Result

For the projected, massless, odd-parity GfE operator at the Schwarzschild point

`ε = β²/M⁴ = 0`,

the first axial overtone `(ell,m,n) = (2,2,1)` has exactly one quasinormal-mode root, counting multiplicity, in the disk

`|Ω - (0.34671099687810464 - 0.27391487535351056 i)| ≤ 5 × 10⁻⁶`.

Because the zero count is one, the enclosed root is simple.

## Certified chain

The standalone verifier checks:

- an ingoing horizon Frobenius series and an all-orders weighted coefficient majorant;
- nonvanishing of the regular horizon factor at the launch point;
- 96-bit fixed-point affine center/sensitivity propagation to the real matching point `z = 3`;
- an outgoing Laurent-Jost endpoint with a positive vertical-ray Volterra damping margin;
- independent affine propagation from the outgoing endpoint to `z = 3`;
- separate nonlinear-remainder transport on both sides to prevent interval wrapping; and
- a Rouché boundary inequality on the stated frequency disk.

The decisive numerical bounds are:

`q_hor ≤ 0.7141139467515436 < 1`

`δ_infinity ≥ 0.5893870317770651 > 0`

`linear lower = 1.033708584346826 × 10⁻⁴`

`total error upper = 7.88238175259142 × 10⁻⁵`

so the certified Rouché margin is

`2.45470409087684 × 10⁻⁵ > 0`.

## Exact claim boundary

This certificate is **epsilon-zero only**. It does not certify an `ε > 0` continuation tube or the derivative `dΩ_221/dε |_(ε=0)`.

It also does not certify the polar sector, axial-polar splitting, or the full unreduced trace-log spectrum, and it does not establish full gravity closure or observational detectability.

## Repository anchors

- verifier: `tools/gfe/verify_gfe_axial_221_epsilon0_simple_root.py`
- machine-readable certificate: `artifacts/chronos/gfe_axial_221_epsilon0_simple_root_certificate.json`
- regression test: `tests/test_gfe_axial_221_epsilon0_simple_root.py`
