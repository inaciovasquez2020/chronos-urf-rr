# GfE axial 220 projected-EFT certificate — 2026-08-05

Status: **certified within the stated projected branch**.

This receipt records the order-reduced, massless, odd-parity GfE calculation for
\(\ell=2\), overtone \(n=0\), with
\(\varepsilon=\beta^2/M^4\in[0,10^{-4}]\).

## Certified chain

- the relative \(O(\beta^2)\) axial source map and structural order reduction;
- the canonical axial master potential;
- shifted-horizon ingoing Frobenius data and a rigorous horizon majorant;
- validated horizon and outgoing-Jost projective propagation to \(z=3\);
- a complex interval-Newton tube containing exactly one simple root for every
  allowed \(\varepsilon\);
- the \(\varepsilon=0\) tangent equations and endpoint tangent disks;
- propagation of \(D_\Omega\) and \(D_\varepsilon\), with \(D_\Omega\ne0\);
- the implicit derivative enclosure

\[
\left.\frac{d\Omega_{220}^{(-)}}{d\varepsilon}\right|_0
\in
(0.027340131607167324-0.014681561963391043i)
+\overline B(0,0.008950737656596899).
\]

Hence the real part of the first-order frequency correction is strictly
positive throughout the certified disk.

## Exact claim boundary

This is **not** a certificate for the polar sector, axial-polar splitting, or
the full unreduced trace-log spectrum. In particular, it does not remove the
additional massive mode of the unreduced operator. The next mathematical
obligation is an independent polar master-potential and endpoint-matching
certificate.

The machine-readable record is
`artifacts/chronos/gfe_axial_220_projected_eft_certificate.json`, the concise
execution receipt is
`artifacts/chronos/gfe_axial_220_projected_eft_runtime_receipt.txt`, and the
reproducible generator is
`tools/gfe/derive_gfe_axial_quadratic_action.sh`.
