# GfE axial 222 epsilon-zero simple root — 2026-09-25

Status: **certified within the projected massless order-reduced axial branch**.

For the Schwarzschild point `epsilon = beta^2/M^4 = 0`, the axial `(ell,m,n)=(2,2,2)` mode has exactly one root, counting multiplicity, in

`|Omega - (0.3010534546123664 - 0.47827698322307185 i)| <= 2e-5`.

Because the zero count is one, the enclosed root is simple.

## Verification chain

The verifier uses the same 96-bit outward-rounded affine/Rouche architecture already used for the certified 221 root:

- ingoing horizon Frobenius recurrence and all-orders majorant;
- nonvanishing regular horizon factor;
- horizon-side affine propagation to `z=3`;
- outgoing Laurent-Jost endpoint with positive damping;
- infinity-side affine propagation to `z=3`; and
- a positive Rouche boundary margin on the stated frequency disk.

The first `5e-6` trial disk failed only at the final Rouche-width gate. The root center mismatch was already tiny, while the propagated proof remainder exceeded the boundary linear term. Widening the disk to `2e-5` closes the same verifier without weakening its error bounds.

## Boundary

This is an **epsilon-zero axial certificate only**. It does not certify finite-epsilon continuation, `dOmega_222/depsilon`, the polar sector, axial-polar splitting, the unreduced trace-log spectrum, or full gravity closure.

## Anchors

- `tools/gfe/verify_gfe_axial_222_epsilon0_simple_root.py`
- `artifacts/chronos/gfe_axial_222_epsilon0_simple_root_certificate.json`
- `tests/test_gfe_axial_222_epsilon0_simple_root.py`
