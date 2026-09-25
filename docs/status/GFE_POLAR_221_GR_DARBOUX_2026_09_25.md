# GfE polar 221 Schwarzschild GR Darboux transfer — 2026-09-25

Status: **certified at the Schwarzschild GR point only**.

The exact Regge–Wheeler/Zerilli Darboux intertwiner transfers the certified axial `(ell,m,n)=(2,2,1)` epsilon-zero root disk to the polar problem. The transferred polar root is therefore unique and simple in the same disk

`|Omega - (0.34671099687810464 - 0.27391487535351056 i)| <= 1.1e-6`.

The verifier rechecks the exact factorization, forward and reverse intertwining, composition identities, endpoint limits, and Wronskian multiplier. The axial disk remains separated from the algebraically special points `Omega = +/- 2 i`, with lower distances greater than `2.30019` and `1.76056`; the inverse Wronskian multiplier has lower bound greater than `4.04963`.

## Boundary

This is a **GR epsilon-zero polar transfer only**. It does not derive a relative `O(beta^2)` polar quadratic action or polar master-potential correction, and it does not certify finite-epsilon polar continuation, a polar frequency derivative, or axial-polar splitting for epsilon greater than zero. The full unreduced trace-log spectrum remains outside this certificate.

## Anchors

- `tools/gfe/verify_gfe_polar_221_gr_darboux.py`
- `artifacts/chronos/gfe_polar_221_gr_darboux_certificate.json`
- `tests/test_gfe_polar_221_gr_darboux_certificate.py`
- dependency: `artifacts/chronos/gfe_axial_221_epsilon0_root_refinement_certificate.json`
