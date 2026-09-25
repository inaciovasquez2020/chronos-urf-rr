# GfE axial 221 epsilon-zero derivative — 2026-09-25

Status: **certified within the projected massless order-reduced axial branch**.

Using the independently refined epsilon-zero root disk and separate horizon/infinity tangent propagation, the verifier certifies

[
\left.\frac{d\Omega_{221}}{d\varepsilon}\right|_{0}
\in
(0.019697184697929637 - 0.06712266263744726 i)
+ \overline B(0, 0.019034322983603982).
]

Hence the certified component bounds include

[
\Re\left.\frac{d\Omega_{221}}{d\varepsilon}\right|_0
> 0.0006628617143256536 > 0
]

and

[
\Im\left.\frac{d\Omega_{221}}{d\varepsilon}\right|_0
< -0.048088339653843196 < 0.
]

This is an independent implicit-function result from

`dΩ/dε = -D_ε/D_Ω`;

the finite-`ε` continuation predictor slope is not used as a substitute for the derivative.

The matching derivative remains nonzero with the certified lower bound

`|D_Ω| ≥ 23.885668804235216`.

## Boundary

This certificate is for the projected massless axial `(ell,m,n)=(2,2,1)` mode at `ε=0`. It does not certify a polar derivative, axial-polar splitting, the full unreduced trace-log spectrum, or full gravity closure.

## Anchors

- `tools/gfe/verify_gfe_axial_221_epsilon0_derivative.py`
- `artifacts/chronos/gfe_axial_221_epsilon0_derivative_certificate.json`
- `tests/test_gfe_axial_221_epsilon0_derivative.py`
- dependency: `artifacts/chronos/gfe_axial_221_epsilon0_root_refinement_certificate.json`
