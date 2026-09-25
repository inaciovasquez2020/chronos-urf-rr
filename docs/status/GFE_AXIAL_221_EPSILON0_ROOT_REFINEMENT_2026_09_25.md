# GfE axial 221 epsilon-zero root refinement — 2026-09-25

Status: **certified within the projected massless order-reduced axial branch**.

The existing Schwarzschild first-overtone root is refined to the disk

`|Ω - (0.34671099687810464 - 0.27391487535351056 i)| ≤ 1.1 × 10⁻⁶`.

The standalone verifier closes a positive Rouché margin and therefore certifies exactly one zero counting multiplicity in this smaller disk. The root is consequently simple.

This refinement exists to support the independent epsilon-zero tangent certificate. It does not replace or weaken the previously certified `5 × 10⁻⁶` root certificate or the finite-`ε` continuation tube.

## Boundary

This result is epsilon-zero and axial only. It does not by itself certify `dΩ_221/dε`, the polar sector, the unreduced trace-log spectrum, or full gravity closure.

## Anchors

- `tools/gfe/verify_gfe_axial_221_epsilon0_root_refinement.py`
- `artifacts/chronos/gfe_axial_221_epsilon0_root_refinement_certificate.json`
- `tests/test_gfe_axial_221_epsilon0_root_refinement.py`
