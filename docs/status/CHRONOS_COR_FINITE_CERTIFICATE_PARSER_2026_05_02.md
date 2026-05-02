# Chronos COR Finite Certificate Parser — 2026-05-02

Status: FINITE CERTIFICATE PARSER / THEOREM ASSUMPTION SURFACE

## Object

This adds a finite certificate parser for the Certified Obstruction Rank quantity

\[
\operatorname{COR}_R(G)=\dim_{\mathbb F_2}(Z_1(G)/L_R(G)).
\]

The certificate records:

- graph identifier,
- field \(\mathbb F_2\),
- radius \(R\),
- vertex count,
- edge count,
- cycle-space dimension,
- local-cycle-subspace rank,
- certified obstruction rank,
- optional finite linear-growth inequality.

## Checked Arithmetic

The parser verifies:

\[
0\le \operatorname{rank}(L_R(G))\le \dim Z_1(G)\le |E(G)|
\]

and

\[
\operatorname{COR}_R(G)=\dim Z_1(G)-\operatorname{rank}(L_R(G)).
\]

If a finite growth claim is enabled, it verifies:

\[
\operatorname{COR}_R(G)\ge \alpha |V(G)|.
\]

## Boundary

This parser checks finite certificate arithmetic only.

It does not recompute \(Z_1(G)\) from raw graph incidence data.

It does not recompute \(L_R(G)\) from local balls.

It does not prove the finite-to-general lift.

It does not prove the locality-to-depth bridge.

It does not prove theorem-level Chronos closure.

## Weakest Next Lemma

The next theorem-level parser upgrade is an incidence-basis certificate:

\[
\partial B_Z=0,\qquad
\operatorname{rank}(B_Z)=\dim Z_1(G),
\]

together with a local-cycle basis certificate for \(L_R(G)\).

