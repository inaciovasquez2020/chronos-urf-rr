# Corrected AEH=1/2 guarded Laurent generator

Date: 2026-08-14

Status: certified within the exact guarded six-state descriptor surface.

## Exact result

For the authoritative corrected descriptor

\[
E(\beta)X'=A(\beta)X,
\]

the exact computation uses

\[
G=\frac{\operatorname{adj}(E)A}{\det E}.
\]

The descriptor determinant has exact beta valuation 3.  The minimum beta
valuation among the nonzero entries of
\(H=\operatorname{adj}(E)A\) is exactly 2.  After the proved common
order-two cancellation, the reduced denominator has valuation 1 and its
regular factor is nonzero at beta zero.  Consequently

\[
G(\beta)=\beta^{-1}G_{-1}+G_0+\beta G_1+\cdots
\]

has exact minimal Laurent order \(-1\).  The matrix \(G_{-1}\) is nonzero,
so this order is minimal; there are no terms below it.

The machine-readable artifact exports every entry valuation, the exact
reduced numerator matrix, the exact reduced scalar denominator, the matrices
\(G_{-1},G_0,G_1\), and a finite all-orders certificate.  If
\(d(\beta)=\sum_j d_j\beta^j\) is the regular denominator, its reciprocal
coefficients are defined by

\[
t_0=d_0^{-1},\qquad
t_n=-d_0^{-1}\sum_{j=1}^{\min(n,\deg d)}d_jt_{n-j},
\]

and convolution with the reduced numerator defines every Laurent
coefficient.  This proves only a sufficiently small guarded punctured
neighborhood; no global beta convergence radius is asserted.

## Exact checks

The deterministic exporter verifies the determinant identity,
\(E\operatorname{adj}(E)A=\det(E)A\), the determinant and numerator beta
valuations, nonvanishing of the regular denominator at zero, exact
reconstruction through \(G_1\), nonvanishing of \(G_{-1}\), and byte-stable
artifact regeneration.  The original descriptor guard is copied unchanged.

The GR reduction remains the already-certified Euler/descriptor-level
statement; the singular ordinary generator is not evaluated at beta zero.

## Scope boundary

This certificate does not construct or certify GQQ, P/Q blocks, invariant
graphs, projectors, complement estimates, horizon closure, or outgoing
closure.  Historical AEH=1 formulas are not used.

Artifacts and verifier:

- `artifacts/chronos/gfe_corrected_AEH_half_laurent_generator.json`
- `artifacts/chronos/gfe_corrected_AEH_half_laurent_generator_receipt.txt`
- `tools/gfe/derive_gfe_corrected_laurent_generator.py`
- `tests/test_gfe_corrected_laurent_generator.py`
