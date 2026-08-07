# Axial Pointwise Price-Law Certificate

**Date:** 2026-08-07
**Certificate commit:** `925563d60a2d682d05e0cd2251a8092432bf4b6c`

## Result

The corrected GfE axial Regge–Wheeler family now carries an analytic
pointwise late-time decay certificate, uniform for

\[
0\le \epsilon \le 10^{-4}.
\]

For axial initial data with no \(\ell=0,1\) component, define

\[
\Lambda_\omega=(1-\Delta_{S^2})^{1/2}
\]

and

\[
\mathcal N_{\mathrm{Price}}
=
\|\langle s\rangle^8\Lambda_\omega^{15}\partial_s\psi_0\|_{L^1}
+
\|\langle s\rangle^8\Lambda_\omega^{15}\psi_0\|_{L^1}
+
\|\langle s\rangle^8\Lambda_\omega^{14}\psi_1\|_{L^1}.
\]

The certified asymptotic statement is

\[
\left\|
\langle s\rangle^{-8}
\left(
\psi(t)+2880t^{-7}\Pi_2A_{2,\epsilon}\Pi_2\psi_1
\right)
\right\|_{L^\infty}
\le
Ct^{-8}(1+\log t)^2\mathcal N_{\mathrm{Price}},
\qquad t\ge2.
\]

Hence, when

\[
\Pi_2A_{2,\epsilon}\Pi_2\psi_1\neq0,
\]

the leading axial tail is

\[
\psi(t)
\sim
-2880\Pi_2A_{2,\epsilon}\Pi_2\psi_1\,t^{-7}.
\]

## Angular-mode structure

The \(\ell=2\) mode supplies the leading \(t^{-7}\) term.

The finite block \(3\le\ell<\ell_0\) is \(O(t^{-9})\), while fixed-order
\(k=8\) semiclassical propagation and spherical-harmonic summation give

\[
\sum_{\ell\ge\ell_0}\Pi_\ell\psi(t)=O(t^{-8}).
\]

Thus all \(\ell\ge3\) modes collectively decay faster than the axial
quadrupole contribution.

## Analytic chain

\[
\text{zero-threshold coercivity}
\Longrightarrow
\text{uniform low-frequency LAP}
\Longrightarrow
\text{high-}L\text{ barrier-top control}
\Longrightarrow
\text{ILED}
\Longrightarrow
\text{threshold spectral expansion}
\Longrightarrow
\text{pointwise Price tail}.
\]

## First-order GfE response pair

The Price-law certificate also admits an exact first-order deformation
test at the GR point.

For the dimensionless \(\ell=2\) zero-energy Schwarzschild operator,
the canonically horizon-normalized threshold solution is

\[
f_0(z)=\frac{z^3}{8},
\qquad
f_0(2)=1,
\qquad
H_0f_0=0.
\]

Writing

\[
H_\epsilon=H_0+\epsilon H_1+O(\epsilon^2),
\]

the exact corrected operator gives

\[
H_1f_0
=
\frac{4(z-2)(231z-524)}{3z^7}.
\]

In particular,

\[
(H_1f_0)(3)
=
\frac{676}{6561}
>0.
\]

For

\[
A_{2,\epsilon}
=
\frac{|f_\epsilon\rangle\langle f_\epsilon|}
{g_\epsilon^2},
\]

write

\[
A_{2,\epsilon}
=
A_0+\epsilon A_1+O(\epsilon^2).
\]

Its first variation is

\[
A_1
=
\frac{|f_1\rangle\langle f_0|
      +|f_0\rangle\langle f_1|}
     {g_0^2}
-
2\frac{g_1}{g_0}A_0.
\]

If \(A_1=0\), the diagonal kernel and \(f_0\neq0\) for \(z>2\)
force

\[
f_1=\frac{g_1}{g_0}f_0.
\]

But differentiating the zero-energy equation gives

\[
H_0f_1=-H_1f_0.
\]

The proposed proportionality would make the left side vanish, while
the exact expression above proves \(H_1f_0\not\equiv0\).
Therefore

\[
A_1\neq0.
\]

Consequently the leading Price coefficient has a nonzero first-order
GfE response,

\[
\left.
\partial_\epsilon
\left(-2880A_{2,\epsilon}\right)
\right|_{\epsilon=0}
=
-2880A_1
\neq0.
\]

Independently, the certified axial \((2,2,0)\) quasinormal-mode tangent
satisfies

\[
\left.
\frac{d\Omega_{220}}{d\epsilon}
\right|_{\epsilon=0}
\in
(0.027340131607167324
-0.014681561963391043\,i)
\pm
0.008950737656596899,
\]

whose real part obeys

\[
\operatorname{Re}
\left(
\left.
\frac{d\Omega_{220}}{d\epsilon}
\right|_{\epsilon=0}
\right)
\ge
0.018389393950570425
>0.
\]

Thus the corrected GfE black-hole response has a certified nontrivial
first-order pair

\[
\boxed{
\left(
A_1,
\left.
\frac{d\Omega_{220}}{d\epsilon}
\right|_{\epsilon=0}
\right),
}
\]

with both components nonzero.

This does not yet define a universal scalar relation between the
late-time tail and the quasinormal frequency. The tail response
\(A_1\) is operator-valued. A scalar tail/QNM consistency relation
requires a canonically specified initial-data or detector functional.

## Scope and boundary

This result concerns the corrected, projected, massless axial GfE operator
family represented by the analytic certificate.

Threshold scattering, Jost/Volterra, Stone-formula, and fixed-order
semiclassical propagation steps are analytic theorem applications. Their
hypotheses are tied to the certified operator geometry and threshold bounds,
but those external functional-analysis results are not themselves formalized
in the repository's proof-assistant layer.

## Repository anchor

Certificate source:

`tools/gfe/derive_gfe_axial_quadratic_action.sh`

Certificate commit:

`925563d60a2d682d05e0cd2251a8092432bf4b6c`

Certificate hash:

`af401d3b7b98f8f832310d90072ac2e1855f82f33f4a52048bee64f2e63d7918`
