# Corrected \(A_{\rm EH}=1/2\) normalized GfE axial action

Date: 2026-08-11

## Result

The normalized Regge-Wheeler-gauge quadratic action has been rebuilt with

\[
L_{\mathrm{full}}
=
\frac12 L_{\mathrm{EH,unit}}
+
\frac{5\beta}{6}L_{\mathrm{Ricci}^2}
+
\beta^2 L_{\mathrm{joint}}.
\]

The action-level normalization gates are:

\[
L_{\mathrm{full}}\big|_{\beta=0}
=
\frac{\lambda}{2}
\left(
Q^2+
\frac{\mu h_0^2}{fr^2}
-
\frac{f\mu h_1^2}{r^2}
\right),
\]

and, for \(\ell=2\), \(\lambda=6\),

\[
[h_{0,r}^2]\,
L_{\mathrm{full}}\big|_{\beta=0}
=
3.
\]

The source rebuild also certifies

\[
[\beta^1]L_{\mathrm{full}}
=
\frac56 L_{\mathrm{Ricci}^2},
\qquad
[\beta^2]L_{\mathrm{full}}
=
L_{\mathrm{joint}}.
\]

The serialized certificate contains no terms beyond \(\beta^2\).

## Provenance correction

The previously recovered generator JSON was generated from a stale
\(A_{\rm EH}=1\) Einstein sector and therefore produced coefficient \(6\)
instead of the required coefficient \(3\).

That stale artifact is not admissible as the source of a corrected finite-\(q\)
\(P/Q\) or \(G_{QQ}\) calculation.

## Boundary

This certificate stops at the normalized action.

It does **not** construct:

- Euler equations,
- the auxiliary Hamiltonian,
- \(P/Q\) blocks,
- \(G_{QQ}\),
- a rank-two projector,
- a global invariant graph,
- or endpoint admissibility.

Any downstream six-state calculation must begin from this corrected
\(A_{\rm EH}=1/2\) normalization and pass its own independent gates.
