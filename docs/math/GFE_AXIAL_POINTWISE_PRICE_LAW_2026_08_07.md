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
