# Local-uniform GfE Riesz-projector limit: proof certificate (2026-10-17)

## Status

This note records the exact algebraic cancellation certificate and the local contour argument it supports. It is **not** a claim of global parameter uniformity or closure of any horizon/outgoing problem. The ordinary-generator descriptor guard has also been checked at the base point: after the fixed substitutions, the leading coefficient of the source descriptor determinant is \(\det E/\beta^3\to875/81\ne0\), and the reduced generator denominator has \(D/\beta\to-125/729\ne0\). These exact nonzero values supply the needed punctured-neighborhood guard near \(M=1\).

## Fixed specialization and exact symbolic gate

Fix
\[
r=3,\qquad \lambda=6,\qquad \omega=i/4,
\]
and retain \(M,z\) as indeterminates. Set
\[
F(M,\beta,z)=zD(M,\beta)I-N(M,\beta).
\]
The GitHub Actions calculation in run [38939067741](https://github.com/inaciovasquez2020/chronos-urf-rr/actions/runs/38939067741) reports the exact symbolic valuations
\[
\operatorname{ord}_{\beta}\det F=4,
\qquad
\operatorname{ord}_{\beta}\bigl(D\operatorname{adj}F\bigr)_{jk}\in\{4,5\}
\quad (1\le j,k\le6).
\]
The gate \(\operatorname{ord}_{\beta}(D\operatorname{adj}F)_{jk}\ge4\) holds for all 36 entries. Since the computation is performed over the generic symbolic parameter field, the coefficients of powers \(\beta^0,\ldots,\beta^3\) vanish identically in the symbolic calculation; this is not merely a finite set of numerical samples.

Artifact SHA-256: `24009f5b1e1c27a2488eb7cd6fa12564140aaa606812f0596ff6243f353d1620`.

The artifact states the ordinary-generator guards \(M\ne0\), \(r\ne0\), \(r-2M\ne0\), \(\lambda\ne0\), \(\beta\ne0\), and nonzero descriptor determinant. At fixed \(r=3\), \(M=3/2\) violates \(r-2M\ne0\) and is outside this guarded calculation. No model-wide exclusion is asserted.

## Local contour argument

Define the cancelled expressions for \(\beta\ne0\):
\[
A(M,\beta,z)=\frac{\det F(M,\beta,z)}{\beta^4},\qquad
B(M,\beta,z)=\frac{D(M,\beta)\operatorname{adj}F(M,\beta,z)}{\beta^4}.
\]
The exact valuation gate removes the apparent common \(\beta^4\) factor from the determinant and every numerator entry. Where the remaining source rational denominators are nonzero, these cancelled expressions extend continuously (and analytically in the complex variables) to \(\beta=0\).

At \(M=1,\beta=0\), the already verified fixed-point calculation gives a limiting denominator proportional to \(144z^2-337\). On the contour \(|z|=2\),
\[
|144z^2-337|\ge 144|z|^2-337=239>0.
\]
Thus the cancelled limiting denominator has no zero on the contour at the base point.

At the base parameters, direct exact evaluation of the source descriptor determinant gives \\det E/\\beta^3\\to875/81, while the reduced denominator has D/\\beta\\to-125/729. Both are nonzero. By continuity, after shrinking the neighborhoods if necessary, the source descriptor determinant is nonzero for sufficiently small \\beta\\ne0 and M near 1, and the reduced denominator has no additional zero there. Compactness of the contour and continuity then give neighborhoods U of M=1 and V of \\beta=0 on which the cancelled denominator A(M,\\beta,z) stays nonzero for |z|=2. Consequently B/A converges uniformly on |z|=2 as \\beta\\to0, locally uniformly for M\\in U. Integrating the contour resolvent gives local-uniform convergence of the corresponding Riesz projectors.

## What this does and does not prove

- **Exact algebraic result:** the symbolic beta-valuation cancellation gate at the stated fixed specialization.
- **Local analytic consequence:** local-uniform Riesz-projector convergence near \\(M=1\\) follows by the compact-contour argument, using the exact nonzero descriptor and reduced-denominator coefficients stated above.
- **Not claimed:** global parameter uniformity; classification of all exceptional specializations; a finite-\(\beta\) invariant projector; a Fredholm resolution; endpoint admissibility; or horizon/outgoing closure.
- **Scope restriction:** the neighborhood is local to \\(M=1\\), and the ordinary-generator representation is used only for sufficiently small nonzero \\(\\beta\\). The argument does not extend across the exceptional locus \\(r-2M=0\\).

## Reproducibility

- Workflow: [run 38939067741](https://github.com/inaciovasquez2020/chronos-urf-rr/actions/runs/38939067741)
- Draft diagnostic PR: [#1318](https://github.com/inaciovasquez2020/chronos-urf-rr/pull/1318)
- Artifact digest: `sha256:24009f5b1e1c27a2488eb7cd6fa12564140aaa606812f0596ff6243f353d1620`

This certificate is intentionally narrow. Do not merge this diagnostic branch until the denominator guard is checked and the resulting proof/test scope is reflected in the PR description.
