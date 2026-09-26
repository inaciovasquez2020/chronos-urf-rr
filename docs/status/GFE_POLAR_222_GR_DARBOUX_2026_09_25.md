# GfE polar 222 Schwarzschild GR Darboux transfer — 2026-09-25

Status: **certified at the Schwarzschild GR point only**.

The exact Regge–Wheeler/Zerilli Darboux intertwiner transfers the certified axial `(ell,m,n)=(2,2,2)` epsilon-zero root disk to the polar problem:

`|Omega - (0.3010534546123664 - 0.47827698322307185 i)| <= 2e-5`.

The transfer preserves endpoint conditions and multiplicity. The disk remains far from the algebraically special points `Omega = +/- 2 i`: the two distance lower bounds are approximately `2.49648` and `1.55120`, and the inverse Wronskian multiplier lower bound is approximately `3.87253`.

## Boundary

This is a **GR epsilon-zero polar transfer only**. It does not derive a relative `O(beta^2)` polar action or master-potential correction, finite-epsilon polar continuation, a polar frequency derivative, or axial-polar splitting at epsilon greater than zero. The unreduced trace-log spectrum remains outside this certificate.

## Anchors

- `tools/gfe/verify_gfe_polar_222_gr_darboux.py`
- `artifacts/chronos/gfe_polar_222_gr_darboux_certificate.json`
- `tests/test_gfe_polar_222_gr_darboux_certificate.py`
- source: `artifacts/chronos/gfe_axial_222_epsilon0_simple_root_certificate.json`
